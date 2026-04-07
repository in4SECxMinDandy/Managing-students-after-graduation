<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $this->call([
            KhoaSeeder::class,
            NganhSeeder::class,
            LopSeeder::class,
            MonHocSeeder::class,
            QuanTriSeeder::class,
        ]);
    }
}
