<?php

namespace App\Modules\TotNghiep\Services;

use App\Modules\HocTap\Services\HocTapService;
use App\Modules\TotNghiep\Models\TotNghiep;

class TotNghiepService
{
    public static string $model = TotNghiep::class;

    public function __construct(
        private HocTapService $hocTapService
    ) {}

    public function xetTotNghiep(string $maSV): TotNghiep
    {
        $gpa = $this->hocTapService->tinhGPA($maSV);
        $xepLoai = TotNghiep::tinhXepLoai($gpa);

        return TotNghiep::updateOrCreate(
            ['MaSV' => $maSV],
            [
                'GPA'     => $gpa,
                'XepLoai' => $xepLoai,
            ]
        );
    }

    public function getKetQua(string $maSV): ?TotNghiep
    {
        return TotNghiep::find($maSV);
    }

    public function getAll()
    {
        return TotNghiep::with('sinhVien')->get();
    }
}
