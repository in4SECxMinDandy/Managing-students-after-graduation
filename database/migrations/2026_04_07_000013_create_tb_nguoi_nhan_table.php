<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('tb_nguoi_nhan', function (Blueprint $table) {
            $table->id();
            $table->string('MaTB', 100);
            $table->string('MaSV', 10);
            $table->boolean('TrangThaiDoc')->default(false);
            $table->date('ThoiGianDoc')->nullable();
            $table->foreign('MaTB')->references('MaTB')->on('thong_bao');
            $table->foreign('MaSV')->references('MaSV')->on('sinh_vien');
            $table->softDeletes();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('tb_nguoi_nhan');
    }
};
