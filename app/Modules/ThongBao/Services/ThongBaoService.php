<?php

namespace App\Modules\ThongBao\Services;

use App\Modules\ThongBao\Models\ThongBao;
use App\Modules\ThongBao\Models\TBNguoiNhan;
use App\Modules\SinhVien\Models\SinhVien;
use Illuminate\Support\Facades\DB;

class ThongBaoService
{
    public function guiThongBao(string $noiDung, string $maAdmin, ?string $loai = 'all'): ThongBao
    {
        return DB::transaction(function () use ($noiDung, $maAdmin, $loai) {
            $thongBao = ThongBao::create([
                'MaTB'    => $this->generateMaTB(),
                'NoiDung' => $noiDung,
                'NgayGui' => now(),
                'MaAdmin' => $maAdmin,
            ]);

            $sinhViens = match ($loai) {
                'khoa' => SinhVien::whereHas('lop.nghanh', fn($q) => $q->where('MaKhoa', request('MaKhoa')))->get(),
                'nganh' => SinhVien::whereHas('lop', fn($q) => $q->where('MaNganh', request('MaNganh')))->get(),
                'lop'   => SinhVien::where('MaLop', request('MaLop'))->get(),
                default => SinhVien::all(),
            };

            foreach ($sinhViens as $sv) {
                TBNguoiNhan::create([
                    'MaTB' => $thongBao->MaTB,
                    'MaSV' => $sv->MaSV,
                ]);
            }

            return $thongBao;
        });
    }

    public function danhSachThongBao(string $maSV)
    {
        return TBNguoiNhan::with('thongBao.quanTri')
            ->where('MaSV', $maSV)
            ->orderByDesc('thongBao.NgayGui')
            ->get();
    }

    public function danhSachTatCa()
    {
        return ThongBao::with('quanTri')->orderByDesc('NgayGui')->get();
    }

    public function danhSachChuaDoc(string $maSV): int
    {
        return TBNguoiNhan::where('MaSV', $maSV)
            ->where('TrangThaiDoc', false)
            ->count();
    }

    public function danhSachGui(): \Illuminate\Database\Eloquent\Collection
    {
        return ThongBao::with('quanTri')->orderByDesc('NgayGui')->get();
    }

    public function markAsRead(int $maTBNN): void
    {
        TBNguoiNhan::find($maTBNN)?->update([
            'TrangThaiDoc'  => true,
            'ThoiGianDoc'   => now(),
        ]);
    }

    private function generateMaTB(): string
    {
        return 'TB' . date('Ymd') . str_pad(random_int(1, 9999), 4, '0', STR_PAD_LEFT);
    }
}
