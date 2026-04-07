<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('quan_tri', function (Blueprint $table) {
            $table->string('MaAdmin', 4)->primary();
            $table->string('TenDN', 20)->unique();
            $table->string('MatKhau', 255);
            $table->softDeletes();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('quan_tri');
    }
};
