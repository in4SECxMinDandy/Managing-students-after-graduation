<?php

namespace Database\Seeders;

use App\Modules\QuanTri\Models\QuanTri;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class QuanTriSeeder extends Seeder
{
    public function run(): void
    {
        QuanTri::updateOrCreate(
            ['MaAdmin' => 'AD01'],
            [
                'TenDN'   => 'admin',
                'MatKhau' => Hash::make('admin123'),
            ]
        );
    }
}
