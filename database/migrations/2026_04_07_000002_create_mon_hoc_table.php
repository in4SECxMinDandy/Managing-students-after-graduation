<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('mon_hoc', function (Blueprint $table) {
            $table->string('MaMH', 7)->primary();
            $table->string('TenMH', 100);
            $table->integer('SoTinChi');
            $table->softDeletes();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('mon_hoc');
    }
};
