<?php

namespace Database\Seeders;

use App\Modules\Khoa\Models\Khoa;
use Illuminate\Database\Seeder;

class KhoaSeeder extends Seeder
{
    public function run(): void
    {
        $khoas = [
            ['MaKhoa' => 'CN', 'TenKhoa' => 'Công nghệ thông tin'],
            ['MaKhoa' => 'KT', 'TenKhoa' => 'Kinh tế'],
            ['MaKhoa' => 'NN', 'TenKhoa' => 'Ngôn ngữ'],
            ['MaKhoa' => 'DL', 'TenKhoa' => 'Du lịch'],
        ];

        foreach ($khoas as $khoa) {
            Khoa::updateOrCreate(['MaKhoa' => $khoa['MaKhoa']], $khoa);
        }
    }
}
