import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1200, 600
DELTA = {  #移動用辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRect, 爆弾Rectの画面内外判定用関数
    引数:こうかとんRect, 爆弾Rect
    戻り値:横方向判定、縦方向判定(True:画面内/False:画面外)
    """
    yoko, tate = True, True
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    if obj_rct.left < 0 or WIDTH <obj_rct.right:
        yoko = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    cry_img = pg.image.load("fig/8.png")
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    clock = pg.time.Clock()
    tmr = 0
    # この下に爆弾の描写
    bd_img = pg.Surface((20, 20))
    bd_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bd_rct):  # こうかとんと爆弾の衝突
            print("Game Over")
            # Game Overとこうかとんの描画
            BG_img = pg.Surface((1200, 600))
            BG_rct = BG_img.get_rect()
            pg.draw.rect(BG_img, (0, 0, 0), (0, 1200, 0, 600))
            BG_img.set_alpha(200)
            screen.blit(BG_img, BG_rct)
            fonto = pg.font.Font(None, 80)
            txt = fonto.render("Game Over", 
                               True, (255, 255, 255))
            txt_rct = txt.get_rect()
            txt_rct.center = WIDTH/2, HEIGHT/2
            screen.blit(cry_img, [390, 270])
            screen.blit(cry_img, [780, 270])
            screen.blit(txt, txt_rct)
            pg.display.update()
            time.sleep(5)   
            return

            
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        # この下に爆弾の動き
        screen.blit(kk_img, kk_rct)
        # bd_rct.move_ip(vx, vy)
        # screen.blit(bd_img, bd_rct)
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        bd_rct.move_ip(vx, vy)
        screen.blit(bd_img, bd_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
