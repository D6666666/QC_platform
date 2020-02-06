from django.db import models

# Create your models here.


class Project(models.Model):
    """
    项目表
    """
    name = models.CharField('名称',max_length=100,blank=False,default='',unique=True)
    describe = models.TextField('描述',default='')
    status = models.BooleanField('状态',default=True)
    create_time = models.DateTimeField('创建时间',auto_now=True)

    def __str__(self):
        return self.name

class Module(models.Model):
    """
    模块表
    """
    project = models.ForeignKey(Project,related_query_name="项目",on_delete=models.CASCADE) #on_delete=models.CASCADE外健联级删除
    name = models.CharField("名称",max_length=100,blank=False,default='')
    describe = models.TextField("描述",default='')
    create_time = models.DateTimeField('创建时间',auto_now=True)

    def __str__(self):
        return self.name
