from django.db import models
import datetime
from django.contrib.auth import get_user_model


User = get_user_model()


class BaseBlogModel(models.Model):
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )    
    created_at = models.DateTimeField(
        'Добавлено', 
        auto_now_add=True, 
        blank=False,)
     
    class Meta: 
        abstract = True
        ordering = ('created_at',)


class Category(BaseBlogModel):
    title = models.CharField(
        max_length=256,
        blank=False, verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        max_length=64, unique=True,
        help_text='Идентификатор страницы для URL; разрешены символы латиницы,'
        ' цифры, дефис и подчёркивание.',
        verbose_name='Идентификатор')   

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(BaseBlogModel):
    name = models.CharField(
        max_length=256, blank=False, verbose_name='Название места')
    
    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name
    

class Post(BaseBlogModel):
    title = models.CharField(
        max_length=256, blank=False, verbose_name='Заголовок'
    )
    text = models.TextField(blank=False, verbose_name='Текст')
    pub_date = models.DateTimeField(
        blank=False,
        help_text='Если установить дату и время в будущем — можно '
        'делать отложенные публикации.',
        verbose_name='Дата и время публикации'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        blank=False,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Категория'
    )

    class Meta(BaseBlogModel.Meta):
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        #ordering = ('-pub-date', )

    def __str__(self):
        return self.title
