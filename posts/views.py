from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from posts.models import Post
from django.db.models import Q, Count, Case, When
# Create your views here.


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6

    context_object_name = 'posts'
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-id').filter(publicado_post=True)
        qs = qs.annotate(
            numero_comentarios = Count(
                Case(
                    When(comentario__publicado_comentario = True, then = 1)
                )
            )
        )
        return qs


class PostBusca(PostIndex):
    template_name = 'posts/post_busca.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        print(self.request.GET.get('termo'))

        if not termo:
            return qs
        qs = qs.filter(
            Q(titulo_posts__icontains=termo)
            Q(autor_posts__ixact=termo)
            Q(conteudo_posts__icontains=termo)
            Q(excerto_posts__icontains=termo)
            Q(titulo_posts__icontains=termo)
            Q(titulo_posts__icontains=termo)
        )
        return qs

class PostCategoria(PostIndex):
    template_name = 'posts/post_categoria.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        categoria = self.kwargs.get('categoria', None)

        if not categoria:
            return qs
        qs = qs.filter(categoria_post__nome_cat__iexact=categoria)

        return qs





class PostDetalhes(UpdateView):
    pass