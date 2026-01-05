from django.shortcuts import render, redirect, get_object_or_404
from .models import Barang, Peminjaman, Penyimpanan
from django.utils import timezone
from datetime import date
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def tentang(request):
    return render(request, 'tentang.html')


@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

def home(request):
    context = {
        'total_barang': Barang.objects.count(),
        'total_peminjaman': Peminjaman.objects.count(),
        'total_penyimpanan': Penyimpanan.objects.count(),
    }
    return render(request, 'home.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrasi berhasil, silakan login.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'auth/register.html', {'form': form})



def daftar_barang(request):
    barang = Barang.objects.all()
    return render(request, 'barang/barang.html', {'barang': barang})

def tambah_barang(request):
    if request.method == 'POST':
        Barang.objects.create(
            nama_barang=request.POST['nama_barang'],
            kategori=request.POST['kategori'],
            stok=request.POST['stok']
        )
        return redirect('/barang/')
    return render(request, 'barang/tambah_barang.html')

def edit_barang(request, id):
    barang = get_object_or_404(Barang, id=id)
    if request.method == 'POST':
        barang.nama_barang = request.POST['nama_barang']
        barang.kategori = request.POST['kategori']
        barang.stok = request.POST['stok']
        barang.save()
        return redirect('/barang/')
    return render(request, 'barang/edit_barang.html', {'barang': barang})

def hapus_barang(request, id):
    barang = get_object_or_404(Barang, id=id)
    if request.method == 'POST':
        barang.delete()
    return redirect('/barang/')

def peminjaman_index(request):
    data = Peminjaman.objects.select_related('barang').all()
    return render(request, 'peminjaman/peminjaman.html', {'data': data})

def tambah_peminjaman(request):
    barang = Barang.objects.all()

    if request.method == 'POST':
        barang_obj = Barang.objects.get(id=request.POST['barang'])
        jumlah = int(request.POST['jumlah'])

        # 🔐 validasi stok
        if jumlah > barang_obj.stok:
            return render(request, 'peminjaman/tambah_peminjaman.html', {
                'barang': barang,
                'error': 'Stok tidak mencukupi'
            })

        # kurangi stok
        barang_obj.stok -= jumlah
        barang_obj.save()

        # simpan peminjaman
        Peminjaman.objects.create(
            nama_peminjam=request.POST['nama_peminjam'],
            barang=barang_obj,
            jumlah=jumlah,
            tanggal_pinjam=request.POST['tanggal_pinjam'],
            status='Dipinjam'
        )

        return redirect('/peminjaman/')

    return render(request, 'peminjaman/tambah_peminjaman.html', {'barang': barang})

def edit_peminjaman(request, id):
    peminjaman = get_object_or_404(Peminjaman, id=id)
    barang_list = Barang.objects.all()

    if request.method == 'POST':
        barang_baru = Barang.objects.get(id=request.POST['barang'])
        jumlah_baru = int(request.POST['jumlah'])

        # 1️⃣ Kembalikan stok lama
        barang_lama = peminjaman.barang
        barang_lama.stok += peminjaman.jumlah
        barang_lama.save()

        # 2️⃣ Validasi stok barang baru
        if jumlah_baru > barang_baru.stok:
            return render(request, 'peminjaman/edit_peminjaman.html', {
                'peminjaman': peminjaman,
                'barang': barang_list,
                'error': 'Stok tidak mencukupi'
            })

        # 3️⃣ Kurangi stok barang baru
        barang_baru.stok -= jumlah_baru
        barang_baru.save()

        # 4️⃣ Update data peminjaman
        peminjaman.nama_peminjam = request.POST['nama_peminjam']
        peminjaman.barang = barang_baru
        peminjaman.jumlah = jumlah_baru
        peminjaman.tanggal_pinjam = request.POST['tanggal_pinjam']
        peminjaman.save()

        return redirect('/peminjaman/')

    return render(request, 'peminjaman/edit_peminjaman.html', {
        'peminjaman': peminjaman,
        'barang': barang_list
    })

def penyimpanan_index(request):
    data = Penyimpanan.objects.select_related('barang').all()
    return render(request, 'penyimpanan/penyimpanan.html', {'data': data})

def tambah_penyimpanan(request):
    barang_list = Barang.objects.all()

    if request.method == 'POST':
        barang = Barang.objects.get(id=request.POST['barang'])
        jumlah = int(request.POST['jumlah'])

        # HITUNG TOTAL BARANG YANG SUDAH DISIMPAN
        total_tersimpan = Penyimpanan.objects.filter(barang=barang)\
                            .aggregate(total=Sum('jumlah'))['total'] or 0

        sisa_stok = barang.stok - total_tersimpan

        # ✅ VALIDASI INI DITARUH DI SINI
        if jumlah > sisa_stok:
            return render(request, 'penyimpanan/tambah_penyimpanan.html', {
                'barang': barang_list,
                'error': f"Jumlah melebihi stok tersedia ({sisa_stok})"
            })

        # SIMPAN JIKA LOLOS VALIDASI
        Penyimpanan.objects.create(
            barang=barang,
            lokasi=request.POST['lokasi'],
            jumlah=jumlah
        )

        return redirect('/penyimpanan/')

    return render(request, 'penyimpanan/tambah_penyimpanan.html', {
        'barang': barang_list
    })

def kembalikan_peminjaman(request, id):
    peminjaman = get_object_or_404(Peminjaman, id=id)

    if peminjaman.status == 'Dipinjam':
        # update status
        peminjaman.status = 'Dikembalikan'
        peminjaman.tanggal_kembali = timezone.now().date()
        peminjaman.save()

        # masuk ke penyimpanan
        Penyimpanan.objects.create(
            barang=peminjaman.barang,
            jumlah=peminjaman.jumlah,
            lokasi='Gudang Utama'
        )

        # kembalikan stok
        barang = peminjaman.barang
        barang.stok += peminjaman.jumlah
        barang.save()

    return redirect('/peminjaman/')

def hapus_peminjaman(request, id):
    peminjaman = get_object_or_404(Peminjaman, id=id)

    if request.method == "POST":
        peminjaman.delete()
        return redirect('/peminjaman/')

def hapus_penyimpanan(request, id):
    penyimpanan = get_object_or_404(Penyimpanan, id=id)
    if request.method == 'POST':
        penyimpanan.delete()
    return redirect('/penyimpanan/')

def edit_penyimpanan(request, id):
    penyimpanan = get_object_or_404(Penyimpanan, id=id)
    barang_list = Barang.objects.all()

    if request.method == 'POST':
        penyimpanan.barang_id = request.POST['barang']
        penyimpanan.lokasi = request.POST['lokasi']
        penyimpanan.jumlah = request.POST['jumlah']
        penyimpanan.save()

        return redirect('/penyimpanan/')

    return render(request, 'penyimpanan/edit_penyimpanan.html', {
        'penyimpanan': penyimpanan,
        'barang': barang_list
    })
    
def kembalikan_barang(request, id):
    peminjaman = get_object_or_404(Peminjaman, id=id)

    if peminjaman.status == 'Dipinjam':
        peminjaman.status = 'Dikembalikan'
        peminjaman.save()

        barang = peminjaman.barang
        barang.stok += peminjaman.jumlah
        barang.save()

        Penyimpanan.objects.create(
            barang=barang,
            jumlah=peminjaman.jumlah,
            lokasi='Gudang',
            tanggal_simpan=date.today()
        )

    return redirect('/peminjaman/')