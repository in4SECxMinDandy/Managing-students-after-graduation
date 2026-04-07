<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('lop', function (Blueprint $table) {
            $table->string('MaLop', 11)->primary();
            $table->string('TenLop', 100)->unique();
            $table->string('MaNganh', 4);
            $table->foreign('MaNganh')->references('MaNganh')->on('nganh');
            $table->softDeletes();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('lop');
    }
};
