const {src, dest, watch, series} = require('gulp')
const plumber = require('gulp-plumber')
const srcmaps = require('gulp-sourcemaps')
const sass = require('gulp-sass')(require('sass'))
const autoprefixer = require('gulp-autoprefixer')
const rename = require('gulp-rename')
const csso = require('gulp-csso')
const server = require('browser-sync')
const imagemin = require('gulp-imagemin')
const svgstore = require('gulp-svgstore')

const pipeline = require('readable-stream').pipeline
const uglify = require('gulp-uglify-es').default
const del = require('del')


function html () {
    return src('src/*.html')
        .pipe(dest('build/'))
}

function css () {
    return src('src/scss/style.scss')
        .pipe(plumber())
        .pipe(srcmaps.init())
        .pipe(sass())
        .pipe(autoprefixer())
        .pipe(csso())
        .pipe(rename('style.min.css'))
        .pipe(srcmaps.write('./'))
        .pipe(dest('build/css/'))
}

function cssNoMin () {
    return src('src/scss/style.scss')
        .pipe(plumber())
        .pipe(sass())
        .pipe(autoprefixer())                
        .pipe(dest('build/css/'))
}

function serve () {
    server.init ({
        server: "build/",
        notify: true,
        open: true,
        cors: true,
        ui: false
    })
    watch('src/scss/**/*.scss', series (css, cssNoMin, refresh))
    watch('src/*.html', series(html, refresh))
}

function refresh (done) {
    server.reload()
    done()
}

function images () {
    return src('src/img/**/*.{png,jpg,jpeg}')
        .pipe(imagemin([
            imagemin.optipng({optimizationLevel: 3}),
            imagemin.mozjpeg({progressive: true})   
        ])).pipe(dest('build/img'))         
}

function sprite () {
    return src('src/img/icon-*.svg')
        .pipe(imagemin([imagemin.svgo()]))
        .pipe(svgstore({
                inlineSvg: true
        }))
        .pipe(rename('sprite.svg'))
        .pipe(dest('build/img'))
}


function js () {
    return pipeline(
        src('src/js/*.js'),
        srcmaps.init(),
        uglify(),
        srcmaps.write('.'),
        rename({suffix: '.min'}),
        dest('build/js')
    )
}

function copy () {
    return src([
        "src/fonts/**/*",
        "src/*.ico",
    ], {
        base: "src"
    })
    .pipe(dest('build'))
}

function clean () {
    return del('build')
}


exports.html = html
exports.css = css
exports['css-nomin'] = cssNoMin
exports.serve = serve
exports.images = images
exports.sprite = sprite
exports.js = js
exports.copy = copy
exports.clean = clean

exports.start = series(
    clean,
    images,
    copy,
    html,
    css,
    cssNoMin,
    sprite,
    js,
    serve
)