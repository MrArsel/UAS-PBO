from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),      # /
    path('tentang/', views.index, name='tentang'),      # /
    path('home/', views.home, name='home'),   # /home/
    path('register/', views.register, name='register'),

    # BARANG
    path('barang/', views.daftar_barang),
    path('barang/tambah/', views.tambah_barang),
    path('barang/edit/<int:id>/', views.edit_barang),
    path('barang/hapus/<int:id>/', views.hapus_barang),


    # PEMINJAMAN
    path('peminjaman/', views.peminjaman_index),
    path('peminjaman/tambah/', views.tambah_peminjaman),
    path('peminjaman/kembalikan/<int:id>/', views.kembalikan_peminjaman),
    path('peminjaman/edit/<int:id>/', views.edit_peminjaman),
    path('peminjaman/hapus/<int:id>/', views.hapus_peminjaman),
    
    # PENYIMPANAN
    path('penyimpanan/', views.penyimpanan_index),
    path('penyimpanan/hapus/<int:id>/', views.hapus_penyimpanan),
    path('penyimpanan/tambah/', views.tambah_penyimpanan),
    path('penyimpanan/edit/<int:id>/', views.edit_penyimpanan),
]
