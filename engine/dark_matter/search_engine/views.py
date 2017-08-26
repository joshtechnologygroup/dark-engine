# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
# TODO: This is rough View
from django.views import View

from dark_matter.query_parser import parser as query_parser
from dark_matter.search_engine import ranker
from dark_matter.search_engine.forms import SearchForm


def search_query(query_string):
    qp = query_parser.Parser(query_string)
    qp.keyword_processor()
    results = ranker.Ranker(qp.query_object).processor()
    for row in results:
        print row['entity_text'].replace('\n', '').replace('\r', '')
        print row['entity_score']


class ProfileList(View):
    form_class = SearchForm
    template_name = 'search.html'

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():
            qp = query_parser.Parser(form.cleaned_data['query'])
            qp.keyword_processor()
            results = ranker.Ranker(qp.query_object).processor()
            response = []
            for row in results:
                response.append(row['entity_text'])

            return render(request, self.template_name, {'results': response, 'form': form})
        return render(request, self.template_name, {'form': self.form_class()})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class()})
