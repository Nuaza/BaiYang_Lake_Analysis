from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class OriginalData(models.Model):
    id = models.IntegerField(primary_key=True)
    所属水系 = models.CharField(max_length=64, default="0")
    所属城市 = models.CharField(max_length=64, default="0")
    断面名称 = models.CharField(max_length=64, default="0")
    日期 = models.CharField(max_length=64, default="0")
    水温 = models.CharField(max_length=64, default="0")
    pH = models.CharField(max_length=64, default="0")
    溶解氧 = models.CharField(max_length=64, default="0")
    高锰酸盐 = models.CharField(max_length=64, default="0")
    COD = models.CharField(max_length=64, default="0")
    BOD = models.CharField(max_length=64, default="0")
    氨氮 = models.CharField(max_length=64, default="0")
    总磷 = models.CharField(max_length=64, default="0")
    总氮 = models.CharField(max_length=64, default="0")
    铜 = models.CharField(max_length=64, default="0")
    锌 = models.CharField(max_length=64, default="0")
    氟化物 = models.CharField(max_length=64, default="0")
    硒 = models.CharField(max_length=64, default="0")
    砷 = models.CharField(max_length=64, default="0")
    汞 = models.CharField(max_length=64, default="0")
    镉 = models.CharField(max_length=64, default="0")
    六价铬 = models.CharField(max_length=64, default="0")
    铅 = models.CharField(max_length=64, default="0")
    氰化物 = models.CharField(max_length=64, default="0")
    挥发酚 = models.CharField(max_length=64, default="0")
    石油类 = models.CharField(max_length=64, default="0")
    阴离子表面活性剂 = models.CharField(max_length=64, default="0")
    硫化物 = models.CharField(max_length=64, default="0")
    粪大肠菌群 = models.CharField(max_length=64, default="0")
    水质类别 = models.CharField(max_length=64, default="Ⅴ类")

    def __str__(self):
        return str(self.id) + "号数据"


class AssociationRulesWithData(models.Model):
    id = models.IntegerField(primary_key=True)
    antecedents = models.CharField(max_length=256, default="")
    consequents = models.CharField(max_length=256, default="")
    ant_support = models.FloatField(max_length=256, default=0)
    con_support = models.FloatField(max_length=256, default=0)
    support = models.FloatField(max_length=256, default=0)
    confidence = models.FloatField(max_length=256, default=0)
    lift = models.FloatField(max_length=256, default=0)
    leverage = models.FloatField(max_length=256, default=0)
    conviction = models.CharField(max_length=256, default="")

    def __str__(self):
        return str(self.id) + "号关联规则"


class AssociationRulesWithStandard(models.Model):
    id = models.IntegerField(primary_key=True)
    antecedents = models.CharField(max_length=256, default="")
    consequents = models.CharField(max_length=256, default="")
    ant_support = models.FloatField(max_length=256, default=0)
    con_support = models.FloatField(max_length=256, default=0)
    support = models.FloatField(max_length=256, default=0)
    confidence = models.FloatField(max_length=256, default=0)
    lift = models.FloatField(max_length=256, default=0)
    leverage = models.FloatField(max_length=256, default=0)
    conviction = models.CharField(max_length=256, default="")

    def __str__(self):
        return str(self.id) + "号关联规则"


class FrequentItemsetsWithData(models.Model):
    id = models.IntegerField(primary_key=True)
    itemsets = models.CharField(max_length=256, default="")
    support = models.CharField(max_length=256, default="")

    def __str__(self):
        return str(self.id) + "号频繁项集"


class FrequentItemsetsWithStandard(models.Model):
    id = models.IntegerField(primary_key=True)
    itemsets = models.CharField(max_length=256, default="")
    support = models.CharField(max_length=256, default="")

    def __str__(self):
        return str(self.id) + "号频繁项集"


class Article(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    context = models.CharField(max_length=1024, default="")

    def __str__(self):
        return str(self.id) + "号文本"
