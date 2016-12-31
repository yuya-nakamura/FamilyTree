"""
People Viewsets
"""
from rest_framework import viewsets
from rest_framework.response import Response
from .models import People
from .serializer import PeopleSerializer, FamilyTreeSerializer


class PeopleViewSet(viewsets.ViewSet):
    """
    People api
    """
    def list(self, request):
        queryset = People.objects.filter(parent=None, marriage_flg=False)
        serializer = PeopleSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        serializer = FamilyTreeSerializer(getFamilyTree(pk), many=True)
        return Response(serializer.data)

def getFamilyTree(people):
    family = list()
    marriages = list()

    generation = 1
    top = People.objects.get(pk=people)
    top.generation = generation
    family.append(top.addColumn(generation, 'top'))
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
        family.append(marriage_people.addColumn(generation, 'top'))

        # 子供を取得する
        children = People.objects.filter(parent__in=[top.pk, marriage_people.pk])
        deep_get_people(children, family, marriages, generation)
    return family

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
        family.append(child.addColumn(generation, parent_node))
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
            family.append(child_marriage_people.addColumn(generation, parent_node))
            married_people.extend([child.pk, child_marriage_people.pk])
    if len(married_people) != 0:
        next_children = People.objects.filter(parent__in=married_people)
        deep_get_people(next_children, family, marriages, generation)
