from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Person(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    bio = models.TextField(blank=True, verbose_name="Биография")

    class Meta:
        verbose_name = "Участник процесса"
        verbose_name_plural = "Участники процесса"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Studio(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название киностудии")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Киностудия"
        verbose_name_plural = "Киностудии"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Film(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название фильма")
    year = models.PositiveIntegerField(verbose_name="Год выпуска")
    description = models.TextField(blank=True, verbose_name="Описание")
    studio = models.ForeignKey(
        Studio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="films",
        verbose_name="Киностудия"
    )
    
    directors = models.ManyToManyField(
        Person, 
        related_name="directed_films", 
        blank=True, 
        verbose_name="Режиссеры"
    )
    actors = models.ManyToManyField(
        Person, 
        related_name="acted_films", 
        blank=True, 
        verbose_name="Актеры"
    )
    producers = models.ManyToManyField(
        Person, 
        related_name="produced_films", 
        blank=True, 
        verbose_name="Продюсеры"
    )

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ["-year", "title"]

    def __str__(self):
        return f"{self.title} ({self.year})"

class MediaTypeChoices(models.TextChoices):
    TRAILER = "trailer", "Трейлер"
    TEASER = "teaser", "Тизер"
    FULL_MOVIE = "full_movie", "Полный фильм"
    POSTER = "poster", "Постер"
    STILL = "still", "Кадр из фильма"

class FilmMedia(models.Model):
    film = models.ForeignKey(
        Film,
        on_delete=models.CASCADE,
        related_name="media_files",
        verbose_name="Фильм"
    )
    media_type = models.CharField(
        max_length=50,
        choices=MediaTypeChoices.choices,
        default=MediaTypeChoices.TRAILER,
        verbose_name="Тип медиа"
    )
    file = models.FileField(
        upload_to="film_media/",
        blank=True,
        null=True,
        verbose_name="Файл"
    )
    external_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Внешняя ссылка"
    )

    class Meta:
        verbose_name = "Медиафайл фильма"
        verbose_name_plural = "Медиафайлы фильмов"

class Review(models.Model):
    film = models.ForeignKey(
        Film,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Фильм"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="movie_reviews",
        verbose_name="Автор рецензии"
    )
    text = models.TextField(verbose_name="Текст рецензии")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Оценка (1-10)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Рецензия"
        verbose_name_plural = "Рецензии"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Рецензия на {self.film.title} от {self.author.username}"