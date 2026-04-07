<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('tot_nghiep', function (Blueprint $table) {
            $table->string('MaSV', 10)->primary();
            $table->decimal('GPA', 4, 2);
            $table->string('XepLoai', 20);
            $table->foreign('MaSV')->references('MaSV')->on('sinh_vien');
            $table->softDeletes();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('tot_nghiep');
    }
};
