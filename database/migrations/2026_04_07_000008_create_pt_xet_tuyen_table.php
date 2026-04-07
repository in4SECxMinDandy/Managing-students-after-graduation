<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('pt_xet_tuyen', function (Blueprint $table) {
            $table->string('MaPTXT', 10)->primary();
            $table->string('MaNganh', 4);
            $table->string('PhuongThuc', 100);
            $table->decimal('Diem', 4, 2);
            $table->string('TrangThai', 100)->default('Chờ duyệt');
            $table->string('MaHSO', 5);
            $table->string('MaAdmin', 4)->nullable();
            $table->foreign('MaNganh')->references('MaNganh')->on('nganh');
            $table->foreign('MaHSO')->references('MaHSO')->on('hso_xet_tuyen');
            $table->foreign('MaAdmin')->references('MaAdmin')->on('quan_tri');
            $table->softDeletes();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('pt_xet_tuyen');
    }
};
