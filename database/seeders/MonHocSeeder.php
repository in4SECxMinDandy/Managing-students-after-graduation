<?php

namespace Database\Seeders;

use App\Modules\MonHoc\Models\MonHoc;
use Illuminate\Database\Seeder;

class MonHocSeeder extends Seeder
{
    public function run(): void
    {
        $monHocs = [
            ['MaMH' => 'CTRR001', 'TenMH' => 'Cơ sở lập trình', 'SoTinChi' => 3],
            ['MaMH' => 'CTRR002', 'TenMH' => 'Cấu trúc dữ liệu và giải thuật', 'SoTinChi' => 4],
            ['MaMH' => 'CTRR003', 'TenMH' => 'Mạng máy tính', 'SoTinChi' => 3],
            ['MaMH' => 'CTRR004', 'TenMH' => 'Cơ sở dữ liệu', 'SoTinChi' => 3],
            ['MaMH' => 'CTRR005', 'TenMH' => 'Lập trình hướng đối tượng', 'SoTinChi' => 3],
            ['MaMH' => 'CTRR006', 'TenMH' => 'Toán cao cấp A1', 'SoTinChi' => 4],
            ['MaMH' => 'CTRR007', 'TenMH' => 'Xác suất thống kê', 'SoTinChi' => 3],
            ['MaMH' => 'CTRR008', 'TenMH' => 'Tiếng Anh chuyên ngành', 'SoTinChi' => 3],
        ];

        foreach ($monHocs as $mh) {
            MonHoc::updateOrCreate(['MaMH' => $mh['MaMH']], $mh);
        }
    }
}
