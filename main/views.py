from django.shortcuts import render
from django.contrib import messages
from .models import (
		UserProfile,
		Blog,
		Portfolio,
		Testimonial,
		Certificate
	)

from django.views import generic
from . forms import ContactForm

class IndexView(generic.TemplateView):
	template_name = "main/index.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		testimonials = Testimonial.objects.filter(is_active=True)
		certificates = Certificate.objects.filter(is_active=True)
		blogs = Blog.objects.filter(is_active=True)
		portfolio = Portfolio.objects.filter(is_active=True)
		
		context["testimonials"] = testimonials
		context["certificates"] = certificates
		context["blogs"] = blogs
		context["portfolio"] = portfolio
		return context


class ContactView(generic.FormView):
	template_name = "main/contact.html"
	form_class = ContactForm
	success_url = "/"
	
	def form_valid(self, form):
		form.save()
		messages.success(self.request, 'Thank you. We will be in touch soon.')
		return super().form_valid(form)


class PortfolioView(generic.ListView):
	model = Portfolio
	template_name = "main/portfolio.html"
	paginate_by = 10

	def get_queryset(self):
		return super().get_queryset().filter(is_active=True)


class PortfolioDetailView(generic.DetailView):
	model = Portfolio
	template_name = "main/portfolio-detail.html"

class BlogView(generic.ListView):
	model = Blog
	template_name = "main/blog.html"
	paginate_by = 10
	
	def get_queryset(self):
		return super().get_queryset().filter(is_active=True)


class BlogDetailView(generic.DetailView):
	model = Blog
	template_name = "main/blog-detail.html"

import openai
from django.http import JsonResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from . import views

openai.api_key = "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"
@csrf_exempt
def chatbot(request):
    # Check if request is POST
    if request.method == 'POST':
        # Get message from request.POST
        message = request.POST.get('message')
        # Call GPT-3 to get response
        response = gpt3_response(message)
        # Render the chatbot template with the response
        return render(request, 'main/chatbot.html', {'response': response})
    else:
        # If request is not POST, render the chatbot template without response
        return render(request, 'main/chatbot.html')

def gpt3_response(message):
    # Set up GPT-3 API parameters
    prompt = f"LamUser: {message}\nAI:"
    model_engine = "text-davinci-002"
    max_tokens = 30
    temperature = 0.8
    # Call GPT-3 API
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        n=1,
        stop=None,
        )
    # Extract response from GPT-3 API output
    response_text = response.choices[0].text.strip()
    # Return response
    return response_text