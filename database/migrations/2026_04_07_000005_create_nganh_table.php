<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('nganh', function (Blueprint $table) {
            $table->string('MaNganh', 4)->primary();
            $table->string('TenNganh', 100);
            $table->string('MaKhoa', 2);
            $table->foreign('MaKhoa')->references('MaKhoa')->on('khoa');
            $table->softDeletes();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('nganh');
    }
};
