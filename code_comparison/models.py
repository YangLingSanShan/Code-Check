from django.db import models
from django.contrib.auth.models import User


class CodeComparisonHistory(models.Model):
    # 历史记录表，目前是一对一比较的记录
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file1 = models.TextField()  # 代码内容
    file2 = models.TextField()
    file1_name = models.CharField(max_length=255)  # 文件名
    file2_name = models.CharField(max_length=255)
    similarity_ratio = models.FloatField()
    check_type = models.CharField(max_length=20, choices=(('normal', '普通查重'), ('ast', '抽象语法树查重')), default=('normal', '普通查重'))
    group_name = models.CharField(max_length=255, default='default group')  # 组名
    marked_as_plagiarism = models.BooleanField(default=False)  # 人工标注抄袭
    diff_content = models.TextField(default='')  # 差异内容
    diff_content_html = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file1_name} vs {self.file2_name} = {self.similarity_ratio}"
