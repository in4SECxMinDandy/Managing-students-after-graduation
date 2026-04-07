<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('hso_xet_tuyen', function (Blueprint $table) {
            $table->string('MaHSO', 5)->primary();
            $table->string('MaTK', 4);
            $table->string('HoTen', 100);
            $table->string('CCCD', 10)->unique();
            $table->string('SDT', 10)->unique();
            $table->foreign('MaTK')->references('MaTK')->on('tk_xet_tuyen');
            $table->softDeletes();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('hso_xet_tuyen');
    }
};
