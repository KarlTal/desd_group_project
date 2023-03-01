from django.urls import path
from UWEFlix import views


home_list_view = views.HomeListView.as_view(
    context_object_name="accounts_list",
    template_name="UWEFlix/home.html",
)

film_list_view = views.FilmListView.as_view(
    context_object_name = "films_list",
    template_name = "UWEFlix/viewFilms.html",
)

club_list_view = views.ClubListView.as_view(
    context_object_name = "clubs_list",
    template_name = "UWEFlix/viewClubs.html",
)


club_rep_list_view = views.ClubRepListView.as_view(
    context_object_name = "club_reps_list",
    template_name = "UWEFlix/viewClubReps.html",
)

urlpatterns = [
    path("",home_list_view, name = "home"),
    path('delete/account/<int:id>',views.Account.deleteAccount,name='deleteAccount'),
    path('addAccounts/',views.Account.addAccount,name="addAccounts"),
    path('update/account/<int:id>',views.Account.updateAccount, name = "updateAccount"),
    path('films/', film_list_view,name='films'),
    path('updateFilm/<int:id>',views.Film.updateFilm, name="updateFilm"),
    path('films/delete/<int:id>',views.Film.deleteFilm,name="deleteFilm"),
    path('films/update/<int:id>',views.Film.updateFilm,name="updateFilm"),
    path('addFilms/',views.Film.addFilm,name="addFilms"),
    path('clubs/',club_list_view,name='clubs'),
    path('clubReps/', club_rep_list_view,name='clubReps'),

]


