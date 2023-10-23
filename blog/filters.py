from django.db.models import Q, F, Count
from blog.models import Post
from django_filters.rest_framework import (NumberFilter,
                                           DateFilter,
                                           FilterSet)


class ProductFilter(FilterSet):
    """
    Filters for model Post.
    """
    ar__exact = NumberFilter(field_name="average_rating")
    ar__lte = NumberFilter(
        field_name="average_rating",
        method="get_lt_including_none"
    )
    ar__gte = NumberFilter(
        field_name="average_rating",
        lookup_expr="gte"
    )
    cr_date__gte = DateFilter(
        field_name="creation_date",
        lookup_expr="date__gte"
    )
    cr_date__lte = DateFilter(
        field_name="creation_date",
        lookup_expr="date__lte"
    )
    cr_date__ex = DateFilter(
        field_name="creation_date",
        lookup_expr="date__exact"
    )
    popularity__exact = NumberFilter(method="get_popularity")
    popularity__gte = NumberFilter(method="get_popularity")
    popularity__lte = NumberFilter(method="get_popularity")

    class Meta:
        model = Post
        fields = ("category", )

    def get_lt_including_none(self, queryset, name, value):
        return queryset.filter(Q(**{f"{name}__lte": value})
                               |
                               Q(**{f"{name}__exact": None}))

    @classmethod
    def get_popular_queryset(cls, queryset):
        """
        Computing the popularity of all posts.
        """
        queryset = queryset.annotate(popularity=(
                F("view_count") +
                (F("amount_comments") * 5) +
                (Count("rating", distinct=True) * 10)
        ))
        return queryset

    def get_popularity(self, queryset, name, value):
        """
        Get a required filter.
        """
        queryset = self.get_popular_queryset(queryset)
        return queryset.filter(**{
            name: value
        })
