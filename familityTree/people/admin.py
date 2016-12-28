# coding: utf-8
"""
adminサイトの設定
"""
import json
from django.contrib import admin
from django.conf.urls import url
from django.template.response import TemplateResponse
from .models import People


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    """
    Peopleの管理サイトの設定です。
    """
    list_display = ('name', 'sex', 'my_url_field')

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
        if obj.parent is None and obj.marriage_flg is False:
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
        family.append(top.toJson(generation, 'top'))
        if top.marriage:
            marriage_people = top.marriage
            father = top if top.sex else marriage_people
            mother = marriage_people if marriage_people.sex is False else top
            marrie = {
                'id': 'g%sf%sm%s' % (generation, father.pk, mother.pk),
                'name': '',
                'display': False,
                'generation': generation,
                'parent_node': 'top',
                'node1': top.name + str(top.pk),
                'node2': marriage_people.name + str(marriage_people.pk)
            }
            family.append(marrie)
            marriages.append(marrie)
            family.append(marriage_people.toJson(generation, 'top'))

            # 子供を取得する
            children = People.objects.filter(parent__in=[top.pk, marriage_people.pk])
            deep_get_people(children, family, marriages, generation)

        context['family'] = json.dumps(family, ensure_ascii=False, indent=2)
        context['marriages'] = json.dumps(marriages, ensure_ascii=False, indent=2)

        return TemplateResponse(request, 'admin/people/people/familytree.html', context=context)

def deep_get_people(children, family, marriages, generation):
    """
    子供を取得するために下に潜っていきます。
    """
    generation += 1
    married_people = list()
    for child in children:
        child.generation = generation
        father = child.parent if child.parent.sex else child.parent.marriage
        mother = child.parent.marriage if child.parent.marriage.sex is False else child.parent
        parent_node = 'g%sf%sm%s' % (generation - 1, father.pk, mother.pk)
        family.append(child.toJson(generation, parent_node))
        if child.marriage:
            child_marriage_people = child.marriage
            child_father = child if child.sex else child_marriage_people
            child_mother = child_marriage_people if child_marriage_people.sex is False else child
            marrie = {
                'id': 'g%sf%sm%s' % (generation, child_father.pk, child_mother.pk),
                'name': '',
                'display': False,
                'generation': generation,
                'parent_node': parent_node,
                'node1': child.name + str(child.pk),
                'node2': child_marriage_people.name + str(child_marriage_people.pk)
            }
            family.append(marrie)
            marriages.append(marrie)
            family.append(child_marriage_people.toJson(generation, parent_node))
            married_people.extend([child.pk, child_marriage_people.pk])
    if len(married_people) != 0:
        next_children = People.objects.filter(parent__in=married_people)
        deep_get_people(next_children, family, marriages, generation)
