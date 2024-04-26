from rest_framework.routers import DefaultRouter
from summary.views import SummarizerView


app_name = "summarize"

router = DefaultRouter()
router.register("summary", SummarizerView, basename="summary")


urlpatterns = router.urls
