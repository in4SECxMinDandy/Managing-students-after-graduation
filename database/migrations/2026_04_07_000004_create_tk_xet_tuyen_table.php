<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('tk_xet_tuyen', function (Blueprint $table) {
            $table->string('MaTK', 4)->primary();
            $table->string('Email', 30)->unique();
            $table->string('MatKhau', 255);
            $table->softDeletes();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('tk_xet_tuyen');
    }
};
