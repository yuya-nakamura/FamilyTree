# coding: utf-8
"""
Peopleモデルの定義
"""
from django.db import models


SEX_LIST = (
    (True, '男'),
    (False, '女')
)


class People(models.Model):
    name = models.CharField(verbose_name='名前', max_length=50)
    name_yomi = models.CharField(verbose_name='読み', max_length=200)
    birthday = models.DateField(verbose_name='誕生日')
    sex = models.BooleanField(verbose_name='性別', choices=SEX_LIST, default=True)
    dieday = models.DateField(verbose_name='没年月日', blank=True, null=True)
    marriage_flg = models.BooleanField(verbose_name='婚約者フラグ', default=False)
    father = models.ForeignKey('self', related_name='father_people', verbose_name='父',
                               blank=True, null=True)
    mother = models.ForeignKey('self', related_name='mother_people', verbose_name='母',
                               blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '人'
        verbose_name_plural = '人々'

    def addColumn(self, generation, parent_node):
        return {
            'id': self.name + str(self.pk),
            'name': self.name,
            'birthday': self.birthday,
            'sex': self.sex,
            'dieday': self.dieday,
            'display': True,
            'generation': generation,
            'marriage_flg': self.marriage_flg,
            'parent_node': parent_node
        }

    def toJson(self, generation, parent_node, marry_count):
        """
        家系図出力用のjsonファイルに変換します。
        """
        disp_dieday = None
        if self.dieday is not None:
            disp_dieday = self.dieday.strftime('%Y/%m/%d')

        return {
            'id': self.name + str(self.pk),
            'name': self.name,
            'birthday': self.birthday.strftime('%Y/%m/%d'),
            'sex': self.sex,
            'dieday': disp_dieday,
            'display': True,
            'marriage': False,
            'generation': generation,
            'marriage_flg': self.marriage_flg,
            'parent_node': parent_node,
            'marry_count': marry_count
        }


class Marriage(models.Model):
    label = models.CharField(verbose_name='名前', max_length=50, blank=True, null=True)
    husband = models.ForeignKey(People, related_name='husband_people', verbose_name='夫')
    wife = models.ForeignKey(People, related_name='wife_people', verbose_name='妻')

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = '婚約'
        verbose_name_plural = '婚約達'

    def toJson(self, generation, parent_node, marry_count):
        return {
            'id': 'g%sf%sm%s' % (generation, self.husband.pk, self.wife.pk),
            'name': self.label,
            'display': False,
            'marriage': True,
            'generation': generation,
            'parent_node': parent_node,
            'marry_count': marry_count,
            'node1': self.husband.name + str(self.husband.pk),
            'node2': self.wife.name + str(self.wife.pk)
        }
