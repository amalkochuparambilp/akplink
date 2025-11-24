from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import LinkPage
from .forms import RegisterForm, LinkForm
from django.db.models import Q

# HOME PAGE
def home(request):
    return render(request, "links/home.html")


# REGISTER
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # create default link page
            LinkPage.objects.create(
                user=user,
                display_name=user.username.capitalize(),
                bio="",
                avatar_initials=user.username[:2].upper()
            )

            login(request, user)
            return redirect(f"/{user.username}/")
    else:
        form = RegisterForm()

    return render(request, "links/register.html", {"form": form})


# LOGIN
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/dashboard/")
    else:
        form = AuthenticationForm()

    return render(request, "links/login.html", {"form": form})


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect("/")


# DASHBOARD: ADD 4 LINKS
@login_required
def dashboard(request):
    # create link page if missing
    if not hasattr(request.user, "link_page"):
        LinkPage.objects.create(
            user=request.user,
            display_name=request.user.username.capitalize(),
            bio="",
            avatar_initials=request.user.username[:2].upper(),
        )

    page = request.user.link_page
    existing_links = list(page.links.all())

    while len(existing_links) < 4:
        existing_links.append(None)

    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            page.links.all().delete()

            for i in range(1, 5):
                title = form.cleaned_data.get(f"title{i}")
                url = form.cleaned_data.get(f"url{i}")

                if title and url:
                    page.links.create(
                        title=title,
                        url=url,
                        order=i,
                        is_active=True,
                    )

            return redirect(f"/{request.user.username}/")
    else:
        initial = {}
        for i, link in enumerate(existing_links, start=1):
            if link:
                initial[f"title{i}"] = link.title
                initial[f"url{i}"] = link.url

        form = LinkForm(initial=initial)

    return render(request, "links/dashboard.html", {"form": form})

# PUBLIC PAGE /<username>/
def user_linktree(request, username):
    from django.contrib.auth.models import User
    from difflib import get_close_matches

    # For profile access
    matches = list(User.objects.values_list("username", flat=True))

    # Try to get real profile
    try:
        page = LinkPage.objects.select_related("user").prefetch_related("links").get(
            user__username=username
        )
    except LinkPage.DoesNotExist:
        # Suggest similar usernames
        suggestions = get_close_matches(username, matches, n=3, cutoff=0.5)

        return render(request, "links/suggestions.html", {
            "username": username,
            "suggestions": suggestions
        })

    links = page.links.filter(is_active=True)

    return render(request, "links/linktree.html", {
        "page": page,
        "links": links,
    })


def search_profiles(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        results = LinkPage.objects.filter(
            Q(user__username__icontains=query) |
            Q(display_name__icontains=query)
        )

    return render(request, "links/search.html", {
        "query": query,
        "results": results,
    })

def user_directory(request):
    pages = LinkPage.objects.select_related("user").order_by("user__username")
    return render(request, "links/directory.html", {"pages": pages})