from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Flight, Passenger
from django.urls import reverse

# Create your views here.
def index(request):
	context = {
		"flighs":Flight.objects.all()

	}
	return render(request, "flights/index.html", context)

def flight(request, flight_id):
	try:
		flight = Flight.objects.get(pk = flight_id)
	except Flight.DoesNotExist:
		raise Http404("Flight doesnot exist")

	context = {
		"flight": flight,
		"passengers": flight.passengers.all(),
		"non_passengers": Passenger.objects.exclude(flights = flight).all()
	} 
	return render(request, "flights/flight.html",context)


def book(request, flight_id):
	try:
		passenger_id = int(request.POST["passenger"]) 
		passenger = Passenger.objects.get(pk = passenger_id)
		flight = Flight.objects.get(pk = flight_id)
	except KeyError:
		return render(request, "flights/error.html", {"message" : "No Selection "})
	except Passenger.DoesNotExist:
		return render(request, "flights/error.html", {"message" : "Passenger does not exist"})
	except Flight.DoesNotExist:
		return render(request, "flights/error.html", {"message" : "Flight does not exist"})

	passenger.flights.add(flight)
	return HttpResponseRedirect(reverse("flight", args = (flight_id,)))
