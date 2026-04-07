<?php

namespace App\Modules\HocTap\Services;

use App\Modules\HocTap\Models\KQHocTap;
use App\Modules\MonHoc\Models\MonHoc;
use Illuminate\Support\Facades\DB;

class HocTapService
{
    public static string $model = KQHocTap::class;

    public function getTranscript(string $maSV)
    {
        return KQHocTap::with('monHoc')
            ->where('MaSV', $maSV)
            ->get();
    }

    public function inputDiem(string $maSV, string $maMH, float $diem): KQHocTap
    {
        return KQHocTap::updateOrCreate(
            ['MaSV' => $maSV, 'MaMH' => $maMH],
            ['Diem' => $diem]
        );
    }

    public function tinhGPA(string $maSV): float
    {
        $ketQua = KQHocTap::with('monHoc')
            ->where('MaSV', $maSV)
            ->get();

        if ($ketQua->isEmpty()) {
            return 0.00;
        }

        $tongDiemThuong = 0;
        $tongTinChi = 0;

        foreach ($ketQua as $kq) {
            $soTinChi = $kq->monHoc->SoTinChi ?? 0;
            $tongDiemThuong += $kq->Diem * $soTinChi;
            $tongTinChi += $soTinChi;
        }

        if ($tongTinChi === 0) {
            return 0.00;
        }

        $gpaThang4 = ($tongDiemThuong / $tongTinChi) / 2.5;

        return round(min(max($gpaThang4, 0.00), 4.00), 2);
    }

    public function getAllDiem()
    {
        return KQHocTap::with(['sinhVien', 'monHoc'])->get();
    }
}
