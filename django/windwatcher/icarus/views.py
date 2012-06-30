# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from icarus.models import Site
import datetime, time
def index(request):
	template = loader.get_template('icarus/index.html')
	site_list = Site.objects.all().order_by('name') 
	dt_utc = datetime.datetime.utcnow()
	# convert UTC to local time
	dt_local = dt_utc - datetime.timedelta(seconds=time.altzone)
	context = Context({
		'datetime': dt_local.strftime("%A the %d, %B %Y at %r"),
		'site_list':site_list,
		})
	return HttpResponse(template.render(context))

def site(request,site="Empty"):
	return HttpResponse("Not ready yet")
