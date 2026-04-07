<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('sinh_vien', function (Blueprint $table) {
            $table->string('MaSV', 10)->primary();
            $table->string('HoTen', 100);
            $table->date('NgaySinh');
            $table->string('Email', 100)->unique();
            $table->string('MatKhau', 255);
            $table->string('MaLop', 11)->nullable();
            $table->string('MaHSO', 5)->nullable();
            $table->foreign('MaLop')->references('MaLop')->on('lop');
            $table->foreign('MaHSO')->references('MaHSO')->on('hso_xet_tuyen');
            $table->softDeletes();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('sinh_vien');
    }
};
