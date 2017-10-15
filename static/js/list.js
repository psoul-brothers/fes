$(document).ready(function(){

    /******************************************
     事前準備
     *******************************************/

        //タブボタンの数を取得
    var tabQuantity = $('.tab__button').length;

    //タブの長さとボディの長さの差分を取得
    var tabExtraDistance = $('.tab').width() - $('.tabContainer').width();

    var isFlick = false;

    var THRESHOLD_PX = 100;



    /******************************************
     スクロール中かどうかの判定
     *******************************************/
    $(window).on('touchstart', onTouchStart); //指が触れたか検知
    $(window).on('touchmove', onTouchMove); //指が動いたか検知
    $(window).on('touchend', onTouchEnd); //指が離れたか検知
    var direction, position;

    //スワイプ開始時の横方向の座標を格納
    function onTouchStart(event) {
        position = getPosition(event);
        direction = ''; //一度リセットする
    }

    //スワイプの方向（left／right）を取得
    function onTouchMove(event) {
        moveRangeX = position - event.originalEvent.touches[0].pageX;
        moveRangeY = position - event.originalEvent.touches[0].pageY;
        if (moveRangeX > THRESHOLD_PX || (-1 * THRESHOLD_PX) > moveRangeX) {
            $(window).on('touchmove.noScroll', function(e) {
                e.preventDefault();
            });
            isFlick = true;
        }
        if (moveRangeY > 5 || (-1 * THRESHOLD_PX) > 5) {
            $(window).on('touchmove.noScroll', function(e) {
                e.preventDefault();
            });
            isFlick = true;
        }
    }

    function onTouchEnd(event) {
        if (isFlick){
            $(window).off('.noScroll');
            isFlick = false;
        }
    }


    /******************************************
     スライダー発動
     *******************************************/
    var slider = $('.contents').bxSlider({
        pager:false,
        controls:false,
        swipeThreshold: THRESHOLD_PX,
        onSlideBefore: function($slideElement, oldIndex, newIndex){
            //スライドする時に関数を呼び出す。newIndexはスライダーの現在地。
            slideChange(newIndex);
        }
    });

    /******************************************
     スライドする時に発動する関数。タブの表示調整を行う。
     *******************************************/
    function slideChange(newIndex){

        //クラスを調整
        $('.tab__button').removeClass('active');
        $('.tab > div:nth-child(' + ( newIndex + 1 ) + ')').addClass('active');

        //スクロールするべき距離を取得。タブ全体の長さ / ( タブの個数 - 1 ) * スライドの現在地
        var scrollDestination = ( tabExtraDistance / (tabQuantity - 1) ) * ( newIndex );

        //スクロール位置を調整
        $('.tabContainer').animate({ scrollLeft: scrollDestination }, 'slow');

    };
    /******************************************
     タブボタンクリックで発動する関数
     *******************************************/

    $('.tab__button').on('click',function(e){

        //何番目の要素かを取ってスライドを移動する
        var nth = $('.tab__button').index(this);
        slider.goToSlide(nth);

        //クリックイベントを無効化
        e.preventDefault();

    })

});