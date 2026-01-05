from django.db import models

class Barang(models.Model):
    nama_barang = models.CharField(max_length=100)
    kategori = models.CharField(max_length=50)
    stok = models.IntegerField()

    def __str__(self):
        return self.nama_barang


class Peminjam(models.Model):
    nama = models.CharField(max_length=100)
    nim = models.CharField(max_length=20)

    def __str__(self):
        return self.nama


class Peminjaman(models.Model):
    nama_peminjam = models.CharField(max_length=100)
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE)
    jumlah = models.IntegerField()
    tanggal_pinjam = models.DateField()
    tanggal_kembali = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Dipinjam', 'Dipinjam'),
            ('Dikembalikan', 'Dikembalikan')
        ],
        default='Dipinjam'
)


    def __str__(self):
        return f"{self.nama_peminjam} - {self.barang.nama_barang}"

class Penyimpanan(models.Model):
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE)
    jumlah = models.IntegerField()
    lokasi = models.CharField(max_length=100)
    tanggal_simpan = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.barang.nama_barang} - {self.lokasi}"
