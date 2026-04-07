<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('thong_bao', function (Blueprint $table) {
            $table->string('MaTB', 100)->primary();
            $table->string('NoiDung', 100);
            $table->date('NgayGui')->useCurrent();
            $table->string('MaAdmin', 4)->nullable();
            $table->foreign('MaAdmin')->references('MaAdmin')->on('quan_tri');
            $table->softDeletes();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('thong_bao');
    }
};
