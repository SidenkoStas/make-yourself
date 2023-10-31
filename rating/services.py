from rating.models import Score
from django.db.models import Q


class RatingServices:
    """
    Service for manage rating.
    Needed 'rating' field in an object model.
    """
    def __init__(self, obj, user):
        self.obj = obj
        self.user = user

    def add_score(self, score):
        """
        Add score to `obj`.
        """
        model_type = self.obj.__class__.__name__
        if score not in (1, 2, 3, 4, 5):
            raise KeyError
        score, is_created = Score.objects.get_or_create(
            user=self.user, model_type=model_type,
            object_id=self.obj.id, defaults={"score": score}
        )
        print(score, is_created)
        return score, is_created

    def remove_score(self):
        """
        Remove score from `obj`.
        """
        model_type = self.obj.__class__.__name__
        Score.objects.filter(
            model_type=model_type, object_id=self.obj.id, user=self.user
        ).delete()

    def get_rating(self) -> int:
        """
        Check `user` score to `obj`.
        """
        if not self.user.is_authenticated:
            return 0
        try:
            model_type = self.obj.__class__.__name__
            score = Score.objects.get(
                model_type=model_type, object_id=self.obj.id, user=self.user
            )
            return score.score
        except:
            return 0
