import difflib
from datetime import datetime
import pytz

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from code_comparison.models import CodeComparisonHistory

from . import ast_check


# 这行要加，等登录登出功能实现完善之后再加上，并且如果未登录时接收到请求，返回一个错误码
# @login_required
@method_decorator(csrf_exempt, name='dispatch')
class CodeComparisonView(View):
    def post(self, request, *args, **kwargs):
        # print('receive post')
        # 根据请求中的参数决定执行哪种比较，默认为一对多
        comparison_type = request.POST.get('comparison_type', 'single_to_multiple')
        # print(comparison_type)
        if comparison_type == 'single_to_multiple':
            return self.single_to_multiple_comparison(request)
        elif comparison_type == 'group':
            return self.group_comparison(request)
        else:
            return JsonResponse({'error': 'Invalid comparison type'}, status=400)

    def single_to_multiple_comparison(self, request):
        files = request.FILES.getlist('files')                  # 其余文件接口files，标准文件接口stdFile
        std_file = request.FILES.get('stdFile')
        check_option = request.POST.get('check_option', 'ast')
        group_name = request.POST.get('classification', 'default group')

        std_content = std_file.read().decode('utf-8')
        similarity_results = []
        user = request.user

        for file in files[0:]:
            file_content = file.read().decode('utf-8')

            if check_option == 'normal':
                ratio = difflib.SequenceMatcher(None, std_content, file_content).quick_ratio()
            else:
                try:
                    ratio = ast_check.calc(std_content, file_content)
                except Exception as e:
                    # print("python file error: ", e)
                    return JsonResponse({'error': 'python file ' + file.name + ' has error.'}, status=400)

            diff_content = get_dif2(std_content, file_content)
            diff_content_html = get_dif(std_content, file_content)

            # 存表
            record_id = CodeComparisonHistory.objects.create(
                user=user,
                file1=std_content,
                file2=file_content,
                file1_name=std_file.name,
                file2_name=file.name,
                similarity_ratio=ratio,
                created_at=datetime.now(),
                diff_content=diff_content,
                diff_content_html=diff_content_html,
                check_type=check_option,
                group_name=group_name,
                marked_as_plagiarism=False,
            ).id

            similarity_results.append({
                'id': record_id,
                'file_name': file.name,
                'similarity_ratio': ratio,
                'diff_content': diff_content,
            })

        similarity_results.sort(key=lambda x: x['similarity_ratio'], reverse=False)

        return JsonResponse({'results': similarity_results})

    def group_comparison(self, request):
        # print(request.FILES)
        # print(request.POST)
        files = request.FILES.getlist('files')
        check_option = request.POST.get('check_option', 'normal')
        groups = []

        # print(files)
        # print(len(files))

        threshold = float(request.POST.get('threshold', 0.8)) # 阈值
        plagiarism_groups = []
        used_indices = set()

        # print('start group comparison')

        for i in range(len(files)):
            if i in used_indices:
                continue
            # print('start compare file ' + i)
            # 为当前代码创建一个新的抄袭嫌疑组
            plagiarism_group = [i]
            file_content = files[i].read().decode('utf-8')
            files[i].seek(0)
            # print(file_content)
            for j in range(i + 1, len(files)):
                if j in used_indices:
                    continue
                file2_content = files[j].read().decode('utf-8')
                files[j].seek(0)

                if check_option == 'normal':
                    ratio = difflib.SequenceMatcher(None, file_content, file2_content).quick_ratio()
                else:
                    try:
                        ratio = ast_check.calc(file_content, file2_content)
                    except Exception as e:
                        return JsonResponse({'error': 'python file ' + files[j].name + ' has error'}, status=400)
                if ratio > threshold:
                    plagiarism_group.append(j)
                    used_indices.add(j)

            if len(plagiarism_group) > 1:
                plagiarism_groups.append(plagiarism_group)
                used_indices.add(i)

        for group in plagiarism_groups:
            group_info = [{'file_id': i, 'file_name': files[i].name, 'file_content': files[i].read().decode('utf-8')} for i in group]
            groups.append({
                'group_info': group_info
            })

        # 新建一个二维矩阵matrix, matrix[i][j]里存放文件i和文件j的json文件比较信息
        matrix = [[None for _ in range(len(files))] for _ in range(len(files))]

        # print(len(files))

        for i in range(len(files)):
            for j in range(len(files)):
                # print(i, j)
                files[i].seek(0)
                files[j].seek(0)
                file1_content = files[i].read().decode('utf-8')
                file2_content = files[j].read().decode('utf-8')
                # print(file1_content)
                # print(file2_content)
                if i != j:
                    ratio = difflib.SequenceMatcher(None, file1_content, file2_content).quick_ratio()
                    matrix[i][j] = {
                        'file1_name': files[i].name,
                        'file2_name': files[j].name,
                        'file1': file1_content,
                        'file2': file2_content,
                        'similarity_ratio': ratio,
                        'diff_content': get_dif2(file1_content, file2_content),
                    }
                else:
                    matrix[i][j] = {
                        'file1_name': files[i].name,
                        'file2_name': files[j].name,
                        'file1': file1_content,
                        'file2': file2_content,
                        'similarity_ratio': 1.0,
                        'diff_content': '',
                    }

        return JsonResponse({'groups': groups, 'matrix': matrix})


@login_required
@require_http_methods(["GET"])
def code_comparison_history(request):
    # 查询当前用户历史记录，查表并返回list
    user_history = CodeComparisonHistory.objects.filter(user=request.user).order_by('-created_at')
    history_list = []
    for history in user_history:
        history_list.append({
            'id': history.id,
            'file1_name': history.file1_name,
            'file2_name': history.file2_name,
            'file1': history.file1,
            'file2': history.file2,
            'similarity_ratio': history.similarity_ratio,
            'created_at': history.created_at,
            'diff_content': history.diff_content,
            'diff_content_html': history.diff_content_html,
        })
    # 按时间从最近的到最远的顺序排序
    history_list.sort(key=lambda x: x['created_at'], reverse=True)
    return JsonResponse({'history': history_list})


@login_required
@require_http_methods(["GET"])
def code_comparison_history_new(request):
    groups = []
    # users_histories = CodeComparisonHistory.objects.all().order_by('-created_at')
    users_histories = CodeComparisonHistory.objects.filter(user=request.user).order_by('-created_at')
    for history in users_histories:
        fl = False
        for group in groups:
            if history.group_name == group['group_name']:
                group['group_list'].append({
                    'id': history.id,
                    'file1_name': history.file1_name,
                    'file2_name': history.file2_name,
                    'file1': history.file1,
                    'file2': history.file2,
                    'similarity_ratio': history.similarity_ratio,
                    'created_at': history.created_at,
                    'diff_content': history.diff_content,
                    'diff_content_html': history.diff_content_html,
                    'check_type': history.check_type,
                    'marked_as_plagiarism': history.marked_as_plagiarism,
                })
                fl = True

        if not fl:
            groups.append({
                'group_name': history.group_name,
                'group_list': [{
                    'id': history.id,
                    'file1_name': history.file1_name,
                    'file2_name': history.file2_name,
                    'file1': history.file1,
                    'file2': history.file2,
                    'similarity_ratio': history.similarity_ratio,
                    'created_at': history.created_at,
                    'diff_content': history.diff_content,
                    'diff_content_html': history.diff_content_html,
                    'check_type': history.check_type,
                    'marked_as_plagiarism': history.marked_as_plagiarism,
                }],
                'created_at': history.created_at
            })
    # 按照 group 的 created_at 从最近的到最远的顺序排序
    groups.sort(key=lambda x: x['created_at'], reverse=True)
    # print(groups)
    return JsonResponse({'groups': groups})


def get_dif(text1, text2):
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    # differ = difflib.Differ()
    differ = difflib.HtmlDiff()
    # diff_result = differ.compare(lines1, lines2)
    # diff_content = '\n'.join(diff_result)
    diff_content = differ.make_table(lines1, lines2, fromdesc='Standard', todesc='Submitted')
    return diff_content


def get_dif2(text1, text2):
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    differ = difflib.Differ()
    # differ = difflib.HtmlDiff()
    diff_result = differ.compare(lines1, lines2)
    diff_content = '\n'.join(diff_result)
    # diff_content = differ.make_table(lines1, lines2, fromdesc='Standard', todesc='Submitted')
    # print(diff_content)
    return diff_content


def submission_details(request, submission_id):
    submission = get_object_or_404(CodeComparisonHistory, id=submission_id)
    similarity_ratio_percent = round(submission.similarity_ratio * 100, 2)
    if submission.check_type[2] == 'n':
        check_type = '普通查重'
    else:
        check_type = '语法树查重'
    submission_dict = {
        "file1": submission.file1,
        "file2": submission.file2,
        "file1_name": submission.file1_name,
        "file2_name": submission.file2_name,
        "similarity_ratio_percent": similarity_ratio_percent,
        "diff_content": submission.diff_content_html,
        "created_at": submission.created_at.astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S'),
        "check_type": check_type,
    }
    return render(request, "submission_details.html", submission_dict)


@login_required
@require_http_methods(["GET"])
def get_groups(request):
    # print('enter get_groups')
    # users_history = CodeComparisonHistory.objects.all()
    users_history = CodeComparisonHistory.objects.filter(user=request.user)
    # 先用 set 去重，然后转换成 list
    groups = set()
    for history in users_history:
        groups.add(history.group_name)
    groups = list(groups)
    groups.sort(reverse=True)
    # print(groups)
    return JsonResponse({'groups': groups})


@login_required
def mark_plagiarism(request):
    submission_id = int(request.POST.get('id'))
    plagiarism = request.POST.get('mark')
    print(submission_id, plagiarism)
    history = get_object_or_404(CodeComparisonHistory, id=submission_id)
    if plagiarism == 'true':
        history.marked_as_plagiarism = True
    else:
        history.marked_as_plagiarism = False
    history.save()
    return JsonResponse({'status': 'success'})
