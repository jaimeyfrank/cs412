from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from .models import *
from .forms import VoterFilterForm
import plotly
import plotly.express as px
import plotly.graph_objects as go
from django.db import models

# Create your views here.

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset()
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['party_affiliation']:
                queryset = queryset.filter(party_affiliation=form.cleaned_data['party_affiliation'])
            if form.cleaned_data['min_dob']:
                queryset = queryset.filter(date_of_birth__gte=form.cleaned_data['min_dob'])
            if form.cleaned_data['max_dob']:
                queryset = queryset.filter(date_of_birth__lte=form.cleaned_data['max_dob'])
            if form.cleaned_data['voter_score']:
                queryset = queryset.filter(voter_score=form.cleaned_data['voter_score'])
            if form.cleaned_data['v20state']:
                queryset = queryset.filter(v20state=True)
            if form.cleaned_data['v21town']:
                queryset = queryset.filter(v21town=True)
            if form.cleaned_data['v21primary']:
                queryset = queryset.filter(v21primary=True)
            if form.cleaned_data['v22general']:
                queryset = queryset.filter(v22general=True)
            if form.cleaned_data['v23town']:
                queryset = queryset.filter(v23town=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = VoterFilterForm(self.request.GET)
        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'


class VoterGraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['party_affiliation']:
                queryset = queryset.filter(party_affiliation=form.cleaned_data['party_affiliation'])
            if form.cleaned_data['min_dob']:
                queryset = queryset.filter(date_of_birth__gte=form.cleaned_data['min_dob'])
            if form.cleaned_data['max_dob']:
                queryset = queryset.filter(date_of_birth__lte=form.cleaned_data['max_dob'])
            if form.cleaned_data['voter_score']:
                queryset = queryset.filter(voter_score=form.cleaned_data['voter_score'])
            if form.cleaned_data['v20state']:
                queryset = queryset.filter(v20state=True)
            if form.cleaned_data['v21town']:
                queryset = queryset.filter(v21town=True)
            if form.cleaned_data['v21primary']:
                queryset = queryset.filter(v21primary=True)
            if form.cleaned_data['v22general']:
                queryset = queryset.filter(v22general=True)
            if form.cleaned_data['v23town']:
                queryset = queryset.filter(v23town=True)
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        # Histogram of Voters by Year of Birth
        voters_by_year = voters.values_list('date_of_birth', flat=True)
        years = [dob.year for dob in voters_by_year]
        fig1 = px.histogram(x=years, nbins=30, title='Distribution of Voters by Year of Birth')
        fig1.update_layout(xaxis_title='Year of Birth', yaxis_title='Count')
        graph1 = plotly.offline.plot(fig1, auto_open=False, output_type='div')

        # Pie Chart of Voters by Party Affiliation
        party_counts = voters.values('party_affiliation').annotate(count=models.Count('party_affiliation'))
        fig2 = px.pie(party_counts, names='party_affiliation', values='count', title='Distribution of Voters by Party Affiliation')
        fig2.update_layout(width=800, height=600)  # Adjust the size of the pie chart
        graph2 = plotly.offline.plot(fig2, auto_open=False, output_type='div')

        # Histogram of Voters by Participation in Elections
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = [voters.filter(**{election: True}).count() for election in elections]
        fig3 = go.Figure(data=[go.Bar(x=elections, y=election_counts)])
        fig3.update_layout(title='Distribution of Voters by Participation in Elections', xaxis_title='Election', yaxis_title='Count')
        graph3 = plotly.offline.plot(fig3, auto_open=False, output_type='div')

        context['graph1'] = graph1
        context['graph2'] = graph2
        context['graph3'] = graph3
        context['filter_form'] = VoterFilterForm(self.request.GET)
        return context