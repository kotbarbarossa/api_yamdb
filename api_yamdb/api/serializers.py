from rest_framework import serializers

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для ревью."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    pub_date = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def get_pub_date(self, obj):
        return obj.pub_date.strftime('%Y-%m-%dT%H:%M:%SZ')
