<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('kq_hoc_tap', function (Blueprint $table) {
            $table->string('MaSV', 10);
            $table->string('MaMH', 7);
            $table->decimal('Diem', 4, 2);
            $table->primary(['MaSV', 'MaMH']);
            $table->foreign('MaSV')->references('MaSV')->on('sinh_vien');
            $table->foreign('MaMH')->references('MaMH')->on('mon_hoc');
            $table->softDeletes();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('kq_hoc_tap');
    }
};
