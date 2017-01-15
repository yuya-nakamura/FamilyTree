# coding: utf-8
"""
adminサイトの設定
"""
import json
from django.contrib import admin
from django.conf.urls import url
from django.template.response import TemplateResponse
from django.db.models import Q
from .models import People, Marriage


class MarriageInline(admin.TabularInline):
    model = Marriage
    fk_name = 'husband'


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    """
    Peopleの管理サイトの設定です。
    """
    list_display = ('name', 'sex', 'my_url_field')
    inlines = [
        MarriageInline
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url(r'^familytree/(?P<people>[-\w]+)/$', self.admin_site.admin_view(self.familytree)),
        ]
        return my_urls + urls

    def my_url_field(self, obj):
        """
        家系図出力用のURLを表示します。
        """
        if obj.father is None and obj.mother is None and obj.marriage_flg is False:
            return '<a href="%s%s">%s</a>' % ('familytree/',
                                              obj.pk, obj.name + '家')
        else:
            return None

    my_url_field.allow_tags = True
    my_url_field.short_description = '家系図'

    def familytree(self, request, people):
        """
        家系図ページのメソッドです。
        """
        context = dict(
            self.admin_site.each_context(request),
        )
        family = list()
        marriages = list()

        generation = 1
        top = People.objects.get(pk=people)
        top.generation = generation
        marries = Marriage.objects.filter(Q(husband=top.pk) | Q(wife=top.pk))
        family.append(top.toJson(generation, 'top', len(marries) - 1))

        marry_count = 0
        for marry in marries:
            marry_json = marry.toJson(generation, 'top', marry_count)
            family.append(marry_json)
            marriages.append(marry_json)
            people = marry.husband if marry.husband.pk != top.pk else marry.wife
            family.append(people.toJson(generation, 'top', marry_count))

            # 子供を取得する
            children = People.objects.filter(father=marry.husband.pk, mother=marry.wife.pk)
            deep_get_people(children, family, marriages, generation)
            marry_count += 1

        context['family'] = json.dumps(family, ensure_ascii=False, indent=2)
        context['marriages'] = json.dumps(marriages, ensure_ascii=False, indent=2)

        return TemplateResponse(request, 'admin/people/people/familytree.html', context=context)

def deep_get_people(children, family, marriages, generation):
    """
    子供を取得するために下に潜っていきます。
    """
    generation += 1
    next_children = list()
    for child in children:
        child.generation = generation
        parent_node = 'g%sf%sm%s' % (generation - 1, child.father.pk, child.mother.pk)
        marries = Marriage.objects.filter(Q(husband=child.pk) | Q(wife=child.pk))
        family.append(child.toJson(generation, parent_node, len(marries) - 1))

        marry_count = 0
        for marry in marries:
            marry_json = marry.toJson(generation, parent_node, marry_count)
            family.append(marry_json)
            marriages.append(marry_json)
            people = marry.husband if marry.husband.pk != child.pk else marry.wife
            family.append(people.toJson(generation, parent_node, marry_count))
            next_children.extend(People.objects.filter(father=marry.husband.pk, mother=marry.wife.pk))
            marry_count += 1
    if len(next_children) != 0:
        deep_get_people(next_children, family, marriages, generation)
