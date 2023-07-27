from django.db import models

# Create your models here.
# accounts/models.py
class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name

class Commodity(models.Model):
    commodity_number = models.BigIntegerField(verbose_name="商品编号", db_column="商品编号")
    three_type = models.CharField(max_length=50, verbose_name="三级分类", db_column="三级分类", db_index=True)
    two_type = models.CharField(max_length=50, verbose_name="二级分类", db_column="二级分类")
    commodity_name = models.TextField(verbose_name="名称", db_column="名称", null=True, blank=True)
    short_name = models.CharField(max_length=255, verbose_name="简称", db_column="简称", null=True, blank=True)
    agent_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="经销价", db_column="经销价")
    finance_sales = models.IntegerField(verbose_name="财务销量", db_column="财务销量")
    income = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="收入", db_column="收入")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="成交单价", db_column="成交单价")
    agent_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="经销成本", db_column="经销成本")
    agent_profit = models.DecimalField(max_digits=6, decimal_places=5, verbose_name="经销毛利", db_column="经销毛利")
    date = models.DateField(verbose_name="日期", db_column="日期")
 
    def __str__(self):
        return str(self.commodity_number)
 
    class Meta:
        db_table = "commodity"
