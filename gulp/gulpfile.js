'use strict';
const gulp = require('gulp');
let sass = require('gulp-sass');
sass.compiler = require('node-sass');

const concat = require('gulp-concat');
const rename = require('gulp-rename');

const src_path = "build/";
const dest_path = "../apps/words/static/words/";

// paths to resources
const paths = {
  scss: src_path + 'scss/**/*.scss',
  scripts: src_path + 'js/**/*.js',
  main: src_path + 'js/main.js',
  plugins: [''],
  css_vendors: [
  // Load Bootstrap
  'node_modules/bootstrap-sass/assets/stylesheets/_bootstrap.scss',
  // Fontawesome
  'node_modules/font-awesome/scss/font-awesome.scss'
  ],
  fonts_vendors: ['node_modules/font-awesome/fonts/fontawesome-webfont.ttf', 'node_modules/font-awesome/fonts/fontawesome-webfont.woff',
            'node_modules/font-awesome/fonts/fontawesome-webfont.woff2', 'node_modules/font-awesome/fonts/fontawesome-webfont.eot', 'node_modules/font-awesome/fonts/fontawesome-webfont.svg']
};

// destinations for resources
const dest = {
  css: dest_path + 'css/',
  scripts: dest_path + 'js/',
  fonts: dest_path + 'fonts/'
};

// process scss file
function styles() {
  return gulp.src(paths.scss)
      .pipe(sass.sync({precision: 10}).on('error', sass.logError))
    .pipe(gulp.dest(dest.css));
}

// process vendors scss file
function styles_vendors() {
  return gulp.src(paths.css_vendors)
      .pipe(sass.sync({precision: 10}).on('error', sass.logError))
    .pipe(concat('vendors.css'))
    .pipe(rename('vendors.css'))
    .pipe(gulp.dest(dest.css));
}

// Combine vendors js, concat, rename, move
// function js_vendors(cb){
//   return gulp.src(paths.vendors)
//     .pipe(concat('vendors.js'))
//     .pipe(rename('vendors.js'))
//     .pipe(gulp.dest(dest.scripts))
// }

function fonts_vendors(){
   return gulp.src(paths.fonts_vendors)
       .pipe(gulp.dest(dest.fonts))
}

function watchTask() {
  gulp.watch([paths.scss].concat(...paths.css_vendors), { interval: 1000 }, gulp.parallel(styles_vendors, styles));
}

exports.watch = watchTask;
exports.build = gulp.parallel(styles, styles_vendors, fonts_vendors);
exports.default = function() {
  gulp.watch([paths.scss].concat(...paths.css_vendors), { interval: 1000 }, gulp.parallel(styles_vendors, styles));
}