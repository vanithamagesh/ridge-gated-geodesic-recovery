
**T_matched.** Matched comparison of refinement procedures applied to identical probability maps (seed 7). Frag: components per image; Betti errors: mean absolute difference to the reference per image; Skel F1: skeleton F1 at 2 DRIVE-equivalent pixels.

| Dataset | Network | Procedure | Dice | Pre | Rec | TCR | clDice | Frag | Betti-0 err | Betti-1 err | Skel F1 | MCC | Acc | Spe | Sen |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DRIVE | U-Net | Threshold 0.5 | 0.8253 | 0.8386 | 0.8125 | 0.6898 | 0.8263 | 75.2 | 72.4 | 30.6 | 0.8993 | 0.8004 | 0.9562 | 0.9772 | 0.8125 |
| DRIVE | U-Net | Threshold selected on validation | 0.8256 | 0.8110 | 0.8406 | 0.7252 | 0.8348 | 73.3 | 70.5 | 28.4 | 0.9049 | 0.7998 | 0.9548 | 0.9714 | 0.8406 |
| DRIVE | U-Net | Threshold 0.25 | 0.8162 | 0.7602 | 0.8810 | 0.7760 | 0.8419 | 73.6 | 70.8 | 26.4 | 0.9087 | 0.7900 | 0.9495 | 0.9595 | 0.8810 |
| DRIVE | U-Net | Hysteresis 0.25 | 0.8168 | 0.7628 | 0.8790 | 0.7692 | 0.8446 | 22.8 | 19.9 | 26.4 | 0.9053 | 0.7905 | 0.9498 | 0.9601 | 0.8790 |
| DRIVE | U-Net | DTI as described (0.5 to 0.3) | 0.8212 | 0.7810 | 0.8658 | 0.7528 | 0.8418 | 28.1 | 25.3 | 27.8 | 0.9043 | 0.7950 | 0.9520 | 0.9646 | 0.8658 |
| DRIVE | U-Net | DTI as released (0.5, 0.3) | 0.8214 | 0.7828 | 0.8641 | 0.7482 | 0.8421 | 28.5 | 25.6 | 27.6 | 0.9023 | 0.7952 | 0.9522 | 0.9650 | 0.8641 |
| DRIVE | U-Net | Dense CRF | 0.8248 | 0.8437 | 0.8067 | 0.6808 | 0.8243 | 74.6 | 71.8 | 31.4 | 0.8963 | 0.8001 | 0.9564 | 0.9782 | 0.8067 |
| DRIVE | U-Net | Closing 3 x 3 | 0.8235 | 0.8302 | 0.8169 | 0.6937 | 0.8233 | 65.8 | 63.0 | 36.0 | 0.8891 | 0.7980 | 0.9554 | 0.9756 | 0.8169 |
| DRIVE | U-Net | RGR | 0.8254 | 0.8316 | 0.8193 | 0.7060 | 0.8291 | 61.0 | 58.1 | 29.6 | 0.9024 | 0.8002 | 0.9559 | 0.9758 | 0.8193 |
| DRIVE | U-Net | RGR on the selected threshold | 0.8253 | 0.8069 | 0.8446 | 0.7348 | 0.8358 | 64.2 | 61.4 | 27.6 | 0.9063 | 0.7995 | 0.9545 | 0.9705 | 0.8446 |
| DRIVE | U-Net | Conservative-gate RGR | 0.8257 | 0.8350 | 0.8165 | 0.6994 | 0.8282 | 63.5 | 60.6 | 30.1 | 0.9009 | 0.8006 | 0.9561 | 0.9765 | 0.8165 |
| DRIVE | U-Net | RGR-P | 0.8237 | 0.8216 | 0.8259 | 0.7245 | 0.8336 | 20.6 | 17.7 | 27.9 | 0.9036 | 0.7980 | 0.9550 | 0.9739 | 0.8259 |
| DRIVE | U-Net | RGR-P, setting re-selected per run | 0.8237 | 0.8216 | 0.8259 | 0.7245 | 0.8336 | 20.6 | 17.7 | 27.9 | 0.9036 | 0.7980 | 0.9550 | 0.9739 | 0.8259 |
| DRIVE | U-Net | RGR-P, recall-oriented | 0.8212 | 0.8118 | 0.8309 | 0.7377 | 0.8339 | 10.3 | 7.5 | 23.8 | 0.9025 | 0.7949 | 0.9540 | 0.9719 | 0.8309 |
| DRIVE | Attention U-Net | Threshold 0.5 | 0.8262 | 0.8397 | 0.8131 | 0.6906 | 0.8270 | 68.2 | 65.3 | 29.2 | 0.8996 | 0.8014 | 0.9565 | 0.9774 | 0.8131 |
| DRIVE | Attention U-Net | Threshold selected on validation | 0.8269 | 0.8152 | 0.8389 | 0.7223 | 0.8343 | 65.8 | 63.0 | 26.9 | 0.9048 | 0.8013 | 0.9553 | 0.9723 | 0.8389 |
| DRIVE | Attention U-Net | Threshold 0.25 | 0.8173 | 0.7612 | 0.8824 | 0.7786 | 0.8434 | 63.6 | 60.8 | 25.4 | 0.9102 | 0.7913 | 0.9498 | 0.9596 | 0.8824 |
| DRIVE | Attention U-Net | Hysteresis 0.25 | 0.8178 | 0.7633 | 0.8807 | 0.7728 | 0.8458 | 18.2 | 15.3 | 25.4 | 0.9070 | 0.7918 | 0.9501 | 0.9602 | 0.8807 |
| DRIVE | Attention U-Net | DTI as described (0.5 to 0.3) | 0.8223 | 0.7819 | 0.8671 | 0.7557 | 0.8427 | 23.5 | 20.6 | 26.4 | 0.9056 | 0.7963 | 0.9523 | 0.9647 | 0.8671 |
| DRIVE | Attention U-Net | DTI as released (0.5, 0.3) | 0.8224 | 0.7838 | 0.8650 | 0.7498 | 0.8430 | 23.7 | 20.9 | 26.7 | 0.9034 | 0.7963 | 0.9524 | 0.9652 | 0.8650 |
| DRIVE | Attention U-Net | Dense CRF | 0.8255 | 0.8448 | 0.8071 | 0.6812 | 0.8246 | 67.5 | 64.7 | 30.0 | 0.8963 | 0.8010 | 0.9566 | 0.9784 | 0.8071 |
| DRIVE | Attention U-Net | Closing 3 x 3 | 0.8244 | 0.8317 | 0.8172 | 0.6942 | 0.8241 | 59.6 | 56.8 | 35.4 | 0.8894 | 0.7991 | 0.9557 | 0.9759 | 0.8172 |
| DRIVE | Attention U-Net | RGR | 0.8263 | 0.8330 | 0.8198 | 0.7067 | 0.8299 | 55.4 | 52.5 | 28.1 | 0.9028 | 0.8013 | 0.9561 | 0.9760 | 0.8198 |
| DRIVE | Attention U-Net | RGR on the selected threshold | 0.8267 | 0.8109 | 0.8430 | 0.7326 | 0.8353 | 56.5 | 53.7 | 26.2 | 0.9065 | 0.8010 | 0.9550 | 0.9713 | 0.8430 |
| DRIVE | Attention U-Net | Conservative-gate RGR | 0.8266 | 0.8365 | 0.8169 | 0.6998 | 0.8290 | 58.2 | 55.4 | 28.6 | 0.9014 | 0.8017 | 0.9564 | 0.9767 | 0.8169 |
| DRIVE | Attention U-Net | RGR-P | 0.8249 | 0.8239 | 0.8258 | 0.7242 | 0.8344 | 17.2 | 14.3 | 26.6 | 0.9038 | 0.7993 | 0.9554 | 0.9743 | 0.8258 |
| DRIVE | Attention U-Net | RGR-P, setting re-selected per run | 0.8249 | 0.8239 | 0.8258 | 0.7242 | 0.8344 | 17.2 | 14.3 | 26.6 | 0.9038 | 0.7993 | 0.9554 | 0.9743 | 0.8258 |
| DRIVE | Attention U-Net | RGR-P, recall-oriented | 0.8224 | 0.8146 | 0.8303 | 0.7367 | 0.8347 | 8.8 | 6.5 | 22.1 | 0.9031 | 0.7962 | 0.9543 | 0.9724 | 0.8303 |
| DRIVE | U-Net++ | Threshold 0.5 | 0.8274 | 0.8364 | 0.8186 | 0.6962 | 0.8282 | 55.8 | 53.0 | 28.0 | 0.9010 | 0.8026 | 0.9565 | 0.9766 | 0.8186 |
| DRIVE | U-Net++ | Threshold selected on validation | 0.8267 | 0.8071 | 0.8473 | 0.7317 | 0.8358 | 52.5 | 49.6 | 27.3 | 0.9061 | 0.8011 | 0.9548 | 0.9705 | 0.8473 |
| DRIVE | U-Net++ | Threshold 0.25 | 0.8174 | 0.7605 | 0.8836 | 0.7792 | 0.8426 | 52.0 | 49.1 | 26.4 | 0.9095 | 0.7915 | 0.9498 | 0.9594 | 0.8836 |
| DRIVE | U-Net++ | Hysteresis 0.25 | 0.8179 | 0.7624 | 0.8820 | 0.7734 | 0.8448 | 15.1 | 12.2 | 26.4 | 0.9068 | 0.7919 | 0.9500 | 0.9599 | 0.8820 |
| DRIVE | U-Net++ | DTI as described (0.5 to 0.3) | 0.8224 | 0.7805 | 0.8692 | 0.7573 | 0.8420 | 19.7 | 16.9 | 27.3 | 0.9065 | 0.7965 | 0.9522 | 0.9643 | 0.8692 |
| DRIVE | U-Net++ | DTI as released (0.5, 0.3) | 0.8226 | 0.7823 | 0.8672 | 0.7517 | 0.8424 | 20.1 | 17.2 | 27.2 | 0.9045 | 0.7965 | 0.9524 | 0.9648 | 0.8672 |
| DRIVE | U-Net++ | Dense CRF | 0.8269 | 0.8416 | 0.8128 | 0.6878 | 0.8264 | 55.1 | 52.2 | 28.8 | 0.8982 | 0.8024 | 0.9567 | 0.9777 | 0.8128 |
| DRIVE | U-Net++ | Closing 3 x 3 | 0.8254 | 0.8287 | 0.8222 | 0.6988 | 0.8253 | 50.7 | 47.9 | 35.5 | 0.8914 | 0.8001 | 0.9557 | 0.9752 | 0.8222 |
| DRIVE | U-Net++ | RGR | 0.8274 | 0.8298 | 0.8250 | 0.7113 | 0.8304 | 45.5 | 42.6 | 27.1 | 0.9036 | 0.8023 | 0.9562 | 0.9753 | 0.8250 |
| DRIVE | U-Net++ | RGR on the selected threshold | 0.8265 | 0.8035 | 0.8508 | 0.7402 | 0.8364 | 44.4 | 41.5 | 26.4 | 0.9072 | 0.8008 | 0.9545 | 0.9697 | 0.8508 |
| DRIVE | U-Net++ | Conservative-gate RGR | 0.8276 | 0.8333 | 0.8220 | 0.7043 | 0.8297 | 47.9 | 45.0 | 27.6 | 0.9026 | 0.8027 | 0.9564 | 0.9760 | 0.8220 |
| DRIVE | U-Net++ | RGR-P | 0.8259 | 0.8222 | 0.8297 | 0.7249 | 0.8334 | 14.2 | 11.4 | 25.9 | 0.9043 | 0.8004 | 0.9555 | 0.9738 | 0.8297 |
| DRIVE | U-Net++ | RGR-P, setting re-selected per run | 0.8256 | 0.8206 | 0.8305 | 0.7273 | 0.8333 | 9.5 | 7.0 | 24.3 | 0.9044 | 0.8000 | 0.9553 | 0.9735 | 0.8305 |
| DRIVE | U-Net++ | RGR-P, recall-oriented | 0.8232 | 0.8128 | 0.8339 | 0.7367 | 0.8331 | 7.0 | 4.7 | 20.1 | 0.9028 | 0.7971 | 0.9544 | 0.9720 | 0.8339 |
| CHASE_DB1 | U-Net | Threshold 0.5 | 0.8086 | 0.7809 | 0.8383 | 0.6897 | 0.8365 | 71.2 | 69.1 | 4.5 | 0.8827 | 0.7891 | 0.9636 | 0.9763 | 0.8383 |
| CHASE_DB1 | U-Net | Threshold selected on validation | 0.8052 | 0.7548 | 0.8630 | 0.7213 | 0.8417 | 81.0 | 78.9 | 4.0 | 0.8841 | 0.7863 | 0.9618 | 0.9717 | 0.8630 |
| CHASE_DB1 | U-Net | Threshold 0.25 | 0.7917 | 0.7077 | 0.8983 | 0.7693 | 0.8414 | 103.0 | 100.9 | 4.4 | 0.8808 | 0.7748 | 0.9567 | 0.9626 | 0.8983 |
| CHASE_DB1 | U-Net | Hysteresis 0.25 | 0.7926 | 0.7101 | 0.8969 | 0.7629 | 0.8469 | 38.2 | 36.1 | 4.4 | 0.8812 | 0.7756 | 0.9570 | 0.9631 | 0.8969 |
| CHASE_DB1 | U-Net | DTI as described (0.5 to 0.3) | 0.7981 | 0.7266 | 0.8853 | 0.7483 | 0.8459 | 42.5 | 40.4 | 4.4 | 0.8822 | 0.7803 | 0.9590 | 0.9664 | 0.8853 |
| CHASE_DB1 | U-Net | DTI as released (0.5, 0.3) | 0.7982 | 0.7282 | 0.8831 | 0.7417 | 0.8464 | 53.8 | 51.6 | 4.2 | 0.8799 | 0.7801 | 0.9591 | 0.9668 | 0.8831 |
| CHASE_DB1 | U-Net | Dense CRF | 0.8080 | 0.7805 | 0.8376 | 0.6837 | 0.8362 | 69.0 | 66.9 | 4.1 | 0.8812 | 0.7885 | 0.9635 | 0.9762 | 0.8376 |
| CHASE_DB1 | U-Net | Closing 3 x 3 | 0.8086 | 0.7800 | 0.8394 | 0.6907 | 0.8371 | 67.9 | 65.8 | 6.0 | 0.8816 | 0.7892 | 0.9636 | 0.9761 | 0.8394 |
| CHASE_DB1 | U-Net | RGR | 0.8021 | 0.7443 | 0.8696 | 0.7388 | 0.8413 | 48.9 | 46.8 | 8.4 | 0.8845 | 0.7833 | 0.9607 | 0.9699 | 0.8696 |
| CHASE_DB1 | U-Net | RGR on the selected threshold | 0.8000 | 0.7329 | 0.8807 | 0.7515 | 0.8433 | 61.8 | 59.6 | 3.5 | 0.8848 | 0.7819 | 0.9597 | 0.9676 | 0.8807 |
| CHASE_DB1 | U-Net | Conservative-gate RGR | 0.8071 | 0.7656 | 0.8535 | 0.7126 | 0.8404 | 57.9 | 55.8 | 4.8 | 0.8841 | 0.7879 | 0.9626 | 0.9736 | 0.8535 |
| CHASE_DB1 | U-Net | RGR-P | 0.8016 | 0.7420 | 0.8717 | 0.7442 | 0.8413 | 32.6 | 30.5 | 9.0 | 0.8837 | 0.7830 | 0.9605 | 0.9694 | 0.8717 |
| CHASE_DB1 | U-Net | RGR-P, setting re-selected per run | 0.8016 | 0.7420 | 0.8717 | 0.7442 | 0.8413 | 32.6 | 30.5 | 9.0 | 0.8837 | 0.7830 | 0.9605 | 0.9694 | 0.8717 |
| CHASE_DB1 | U-Net | RGR-P, recall-oriented | 0.8001 | 0.7361 | 0.8764 | 0.7579 | 0.8372 | 14.8 | 12.6 | 14.1 | 0.8807 | 0.7817 | 0.9599 | 0.9683 | 0.8764 |
| CHASE_DB1 | Attention U-Net | Threshold 0.5 | 0.8101 | 0.7909 | 0.8301 | 0.6743 | 0.8343 | 74.2 | 72.1 | 5.5 | 0.8794 | 0.7907 | 0.9643 | 0.9779 | 0.8301 |
| CHASE_DB1 | Attention U-Net | Threshold selected on validation | 0.8090 | 0.7686 | 0.8538 | 0.7025 | 0.8399 | 85.4 | 83.2 | 5.0 | 0.8845 | 0.7899 | 0.9631 | 0.9741 | 0.8538 |
| CHASE_DB1 | Attention U-Net | Threshold 0.25 | 0.7963 | 0.7190 | 0.8921 | 0.7548 | 0.8428 | 96.6 | 94.5 | 4.1 | 0.8831 | 0.7789 | 0.9582 | 0.9649 | 0.8921 |
| CHASE_DB1 | Attention U-Net | Hysteresis 0.25 | 0.7970 | 0.7211 | 0.8907 | 0.7489 | 0.8472 | 39.6 | 37.5 | 4.1 | 0.8818 | 0.7795 | 0.9584 | 0.9653 | 0.8907 |
| CHASE_DB1 | Attention U-Net | DTI as described (0.5 to 0.3) | 0.8023 | 0.7378 | 0.8792 | 0.7336 | 0.8457 | 43.9 | 41.8 | 3.8 | 0.8826 | 0.7842 | 0.9603 | 0.9685 | 0.8792 |
| CHASE_DB1 | Attention U-Net | DTI as released (0.5, 0.3) | 0.8024 | 0.7394 | 0.8772 | 0.7272 | 0.8464 | 48.9 | 46.8 | 3.6 | 0.8809 | 0.7842 | 0.9604 | 0.9688 | 0.8772 |
| CHASE_DB1 | Attention U-Net | Dense CRF | 0.8094 | 0.7903 | 0.8294 | 0.6680 | 0.8335 | 69.4 | 67.2 | 4.6 | 0.8776 | 0.7899 | 0.9642 | 0.9778 | 0.8294 |
| CHASE_DB1 | Attention U-Net | Closing 3 x 3 | 0.8103 | 0.7903 | 0.8313 | 0.6754 | 0.8346 | 69.1 | 67.0 | 5.9 | 0.8792 | 0.7909 | 0.9643 | 0.9778 | 0.8313 |
| CHASE_DB1 | Attention U-Net | RGR | 0.8041 | 0.7532 | 0.8625 | 0.7230 | 0.8406 | 51.2 | 49.1 | 7.5 | 0.8830 | 0.7851 | 0.9615 | 0.9715 | 0.8625 |
| CHASE_DB1 | Attention U-Net | RGR on the selected threshold | 0.8034 | 0.7440 | 0.8732 | 0.7356 | 0.8424 | 63.1 | 61.0 | 3.4 | 0.8848 | 0.7850 | 0.9609 | 0.9697 | 0.8732 |
| CHASE_DB1 | Attention U-Net | Conservative-gate RGR | 0.8092 | 0.7755 | 0.8459 | 0.6960 | 0.8381 | 60.8 | 58.6 | 4.9 | 0.8819 | 0.7900 | 0.9635 | 0.9753 | 0.8459 |
| CHASE_DB1 | Attention U-Net | RGR-P | 0.8043 | 0.7512 | 0.8655 | 0.7309 | 0.8425 | 34.8 | 32.6 | 8.2 | 0.8834 | 0.7854 | 0.9614 | 0.9711 | 0.8655 |
| CHASE_DB1 | Attention U-Net | RGR-P, setting re-selected per run | 0.8043 | 0.7512 | 0.8655 | 0.7309 | 0.8425 | 34.8 | 32.6 | 8.2 | 0.8834 | 0.7854 | 0.9614 | 0.9711 | 0.8655 |
| CHASE_DB1 | Attention U-Net | RGR-P, recall-oriented | 0.8030 | 0.7451 | 0.8705 | 0.7456 | 0.8392 | 15.0 | 12.9 | 11.5 | 0.8805 | 0.7843 | 0.9609 | 0.9700 | 0.8705 |
| CHASE_DB1 | U-Net++ | Threshold 0.5 | 0.8100 | 0.7900 | 0.8311 | 0.6919 | 0.8350 | 67.4 | 65.2 | 5.4 | 0.8853 | 0.7906 | 0.9643 | 0.9777 | 0.8311 |
| CHASE_DB1 | U-Net++ | Threshold selected on validation | 0.8082 | 0.7625 | 0.8597 | 0.7262 | 0.8409 | 74.4 | 72.2 | 4.5 | 0.8873 | 0.7893 | 0.9626 | 0.9730 | 0.8597 |
| CHASE_DB1 | U-Net++ | Threshold 0.25 | 0.7975 | 0.7197 | 0.8941 | 0.7712 | 0.8432 | 88.4 | 86.2 | 4.4 | 0.8871 | 0.7803 | 0.9584 | 0.9649 | 0.8941 |
| CHASE_DB1 | U-Net++ | Hysteresis 0.25 | 0.7979 | 0.7214 | 0.8926 | 0.7643 | 0.8470 | 37.1 | 35.0 | 4.4 | 0.8857 | 0.7806 | 0.9586 | 0.9653 | 0.8926 |
| CHASE_DB1 | U-Net++ | DTI as described (0.5 to 0.3) | 0.8029 | 0.7378 | 0.8804 | 0.7494 | 0.8457 | 41.4 | 39.2 | 4.1 | 0.8865 | 0.7848 | 0.9604 | 0.9685 | 0.8804 |
| CHASE_DB1 | U-Net++ | DTI as released (0.5, 0.3) | 0.8029 | 0.7394 | 0.8784 | 0.7433 | 0.8466 | 46.1 | 44.0 | 4.5 | 0.8848 | 0.7847 | 0.9605 | 0.9688 | 0.8784 |
| CHASE_DB1 | U-Net++ | Dense CRF | 0.8096 | 0.7897 | 0.8305 | 0.6854 | 0.8346 | 65.1 | 63.0 | 5.2 | 0.8837 | 0.7901 | 0.9642 | 0.9777 | 0.8305 |
| CHASE_DB1 | U-Net++ | Closing 3 x 3 | 0.8103 | 0.7895 | 0.8322 | 0.6932 | 0.8361 | 65.1 | 63.0 | 5.4 | 0.8843 | 0.7909 | 0.9643 | 0.9776 | 0.8322 |
| CHASE_DB1 | U-Net++ | RGR | 0.8045 | 0.7525 | 0.8641 | 0.7387 | 0.8399 | 49.0 | 46.9 | 4.5 | 0.8870 | 0.7855 | 0.9615 | 0.9713 | 0.8641 |
| CHASE_DB1 | U-Net++ | RGR on the selected threshold | 0.8036 | 0.7416 | 0.8769 | 0.7537 | 0.8424 | 57.4 | 55.2 | 3.6 | 0.8865 | 0.7853 | 0.9607 | 0.9692 | 0.8769 |
| CHASE_DB1 | U-Net++ | Conservative-gate RGR | 0.8093 | 0.7746 | 0.8473 | 0.7135 | 0.8382 | 55.8 | 53.6 | 3.8 | 0.8864 | 0.7901 | 0.9634 | 0.9751 | 0.8473 |
| CHASE_DB1 | U-Net++ | RGR-P | 0.8044 | 0.7504 | 0.8668 | 0.7457 | 0.8409 | 31.6 | 29.5 | 5.1 | 0.8872 | 0.7856 | 0.9614 | 0.9709 | 0.8668 |
| CHASE_DB1 | U-Net++ | RGR-P, setting re-selected per run | 0.8042 | 0.7486 | 0.8687 | 0.7512 | 0.8400 | 20.5 | 18.4 | 8.4 | 0.8862 | 0.7855 | 0.9613 | 0.9706 | 0.8687 |
| CHASE_DB1 | U-Net++ | RGR-P, recall-oriented | 0.8033 | 0.7451 | 0.8713 | 0.7585 | 0.8392 | 15.6 | 13.5 | 10.0 | 0.8846 | 0.7847 | 0.9609 | 0.9700 | 0.8713 |
| STARE | U-Net | Threshold 0.5 | 0.8423 | 0.8737 | 0.8131 | 0.7772 | 0.8773 | 69.6 | 64.9 | 19.4 | 0.9189 | 0.8260 | 0.9693 | 0.9868 | 0.8131 |
| STARE | U-Net | Threshold selected on validation | 0.8459 | 0.8512 | 0.8406 | 0.8050 | 0.8841 | 66.1 | 61.4 | 17.9 | 0.9229 | 0.8287 | 0.9691 | 0.9835 | 0.8406 |
| STARE | U-Net | Threshold 0.25 | 0.8430 | 0.8076 | 0.8816 | 0.8447 | 0.8913 | 68.5 | 63.8 | 14.3 | 0.9273 | 0.8255 | 0.9669 | 0.9764 | 0.8816 |
| STARE | U-Net | Hysteresis 0.25 | 0.8434 | 0.8096 | 0.8801 | 0.8398 | 0.8935 | 27.1 | 22.4 | 14.3 | 0.9253 | 0.8259 | 0.9670 | 0.9768 | 0.8801 |
| STARE | U-Net | DTI as described (0.5 to 0.3) | 0.8455 | 0.8255 | 0.8664 | 0.8271 | 0.8907 | 30.6 | 25.9 | 15.7 | 0.9236 | 0.8280 | 0.9681 | 0.9795 | 0.8664 |
| STARE | U-Net | DTI as released (0.5, 0.3) | 0.8450 | 0.8268 | 0.8640 | 0.8219 | 0.8900 | 34.2 | 29.5 | 15.4 | 0.9216 | 0.8274 | 0.9680 | 0.9797 | 0.8640 |
| STARE | U-Net | Dense CRF | 0.8417 | 0.8760 | 0.8099 | 0.7696 | 0.8756 | 66.1 | 61.4 | 19.4 | 0.9163 | 0.8254 | 0.9693 | 0.9871 | 0.8099 |
| STARE | U-Net | Closing 3 x 3 | 0.8426 | 0.8689 | 0.8179 | 0.7805 | 0.8763 | 60.4 | 55.7 | 22.5 | 0.9156 | 0.8260 | 0.9692 | 0.9862 | 0.8179 |
| STARE | U-Net | RGR | 0.8442 | 0.8608 | 0.8283 | 0.8118 | 0.8855 | 47.0 | 42.3 | 18.6 | 0.9237 | 0.8273 | 0.9692 | 0.9850 | 0.8283 |
| STARE | U-Net | RGR on the selected threshold | 0.8462 | 0.8436 | 0.8489 | 0.8239 | 0.8876 | 51.3 | 46.6 | 17.4 | 0.9250 | 0.8289 | 0.9689 | 0.9823 | 0.8489 |
| STARE | U-Net | Conservative-gate RGR | 0.8439 | 0.8696 | 0.8196 | 0.7915 | 0.8813 | 56.9 | 52.2 | 19.2 | 0.9209 | 0.8274 | 0.9694 | 0.9862 | 0.8196 |
| STARE | U-Net | RGR-P | 0.8443 | 0.8561 | 0.8328 | 0.8207 | 0.8874 | 24.7 | 20.0 | 17.3 | 0.9236 | 0.8272 | 0.9690 | 0.9843 | 0.8328 |
| STARE | U-Net | RGR-P, setting re-selected per run | 0.8443 | 0.8561 | 0.8328 | 0.8207 | 0.8874 | 24.7 | 20.0 | 17.3 | 0.9236 | 0.8272 | 0.9690 | 0.9843 | 0.8328 |
| STARE | U-Net | RGR-P, recall-oriented | 0.8424 | 0.8479 | 0.8370 | 0.8313 | 0.8855 | 10.9 | 7.6 | 13.0 | 0.9214 | 0.8249 | 0.9684 | 0.9832 | 0.8370 |
| STARE | Attention U-Net | Threshold 0.5 | 0.8474 | 0.8712 | 0.8250 | 0.7900 | 0.8820 | 66.6 | 61.9 | 17.7 | 0.9240 | 0.8312 | 0.9700 | 0.9863 | 0.8250 |
| STARE | Attention U-Net | Threshold selected on validation | 0.8496 | 0.8502 | 0.8490 | 0.8140 | 0.8869 | 65.0 | 60.3 | 18.1 | 0.9276 | 0.8328 | 0.9697 | 0.9832 | 0.8490 |
| STARE | Attention U-Net | Threshold 0.25 | 0.8445 | 0.8035 | 0.8900 | 0.8553 | 0.8917 | 65.7 | 61.0 | 15.4 | 0.9291 | 0.8274 | 0.9669 | 0.9756 | 0.8900 |
| STARE | Attention U-Net | Hysteresis 0.25 | 0.8451 | 0.8056 | 0.8886 | 0.8507 | 0.8947 | 24.4 | 19.7 | 15.4 | 0.9277 | 0.8280 | 0.9671 | 0.9760 | 0.8886 |
| STARE | Attention U-Net | DTI as described (0.5 to 0.3) | 0.8479 | 0.8216 | 0.8758 | 0.8392 | 0.8927 | 28.3 | 23.6 | 16.2 | 0.9275 | 0.8307 | 0.9683 | 0.9787 | 0.8758 |
| STARE | Attention U-Net | DTI as released (0.5, 0.3) | 0.8477 | 0.8229 | 0.8739 | 0.8341 | 0.8924 | 28.9 | 24.2 | 16.3 | 0.9260 | 0.8305 | 0.9683 | 0.9789 | 0.8739 |
| STARE | Attention U-Net | Dense CRF | 0.8469 | 0.8734 | 0.8219 | 0.7824 | 0.8804 | 65.7 | 61.0 | 17.9 | 0.9219 | 0.8307 | 0.9700 | 0.9866 | 0.8219 |
| STARE | Attention U-Net | Closing 3 x 3 | 0.8475 | 0.8667 | 0.8292 | 0.7933 | 0.8808 | 58.7 | 54.0 | 21.5 | 0.9213 | 0.8311 | 0.9699 | 0.9857 | 0.8292 |
| STARE | Attention U-Net | RGR | 0.8480 | 0.8564 | 0.8397 | 0.8229 | 0.8887 | 42.9 | 38.2 | 16.9 | 0.9272 | 0.8312 | 0.9696 | 0.9842 | 0.8397 |
| STARE | Attention U-Net | RGR on the selected threshold | 0.8492 | 0.8408 | 0.8578 | 0.8344 | 0.8901 | 46.4 | 41.7 | 17.8 | 0.9284 | 0.8322 | 0.9693 | 0.9818 | 0.8578 |
| STARE | Attention U-Net | Conservative-gate RGR | 0.8483 | 0.8664 | 0.8310 | 0.8028 | 0.8848 | 51.9 | 47.2 | 17.3 | 0.9250 | 0.8319 | 0.9700 | 0.9856 | 0.8310 |
| STARE | Attention U-Net | RGR-P | 0.8472 | 0.8510 | 0.8434 | 0.8323 | 0.8903 | 20.8 | 16.1 | 15.8 | 0.9269 | 0.8302 | 0.9693 | 0.9834 | 0.8434 |
| STARE | Attention U-Net | RGR-P, setting re-selected per run | 0.8472 | 0.8510 | 0.8434 | 0.8323 | 0.8903 | 20.8 | 16.1 | 15.8 | 0.9269 | 0.8302 | 0.9693 | 0.9834 | 0.8434 |
| STARE | Attention U-Net | RGR-P, recall-oriented | 0.8456 | 0.8435 | 0.8477 | 0.8430 | 0.8892 | 8.8 | 5.3 | 11.6 | 0.9257 | 0.8282 | 0.9688 | 0.9824 | 0.8477 |
| STARE | U-Net++ | Threshold 0.5 | 0.8499 | 0.8786 | 0.8229 | 0.7933 | 0.8848 | 51.0 | 46.3 | 18.4 | 0.9252 | 0.8342 | 0.9707 | 0.9872 | 0.8229 |
| STARE | U-Net++ | Threshold selected on validation | 0.8538 | 0.8551 | 0.8525 | 0.8219 | 0.8909 | 54.0 | 49.3 | 16.4 | 0.9300 | 0.8374 | 0.9705 | 0.9838 | 0.8525 |
| STARE | U-Net++ | Threshold 0.25 | 0.8507 | 0.8151 | 0.8895 | 0.8591 | 0.8940 | 57.3 | 52.6 | 15.1 | 0.9317 | 0.8341 | 0.9685 | 0.9774 | 0.8895 |
| STARE | U-Net++ | Hysteresis 0.25 | 0.8512 | 0.8172 | 0.8881 | 0.8541 | 0.8969 | 21.6 | 16.9 | 15.1 | 0.9309 | 0.8346 | 0.9687 | 0.9777 | 0.8881 |
| STARE | U-Net++ | DTI as described (0.5 to 0.3) | 0.8533 | 0.8326 | 0.8749 | 0.8407 | 0.8953 | 24.1 | 19.4 | 15.7 | 0.9301 | 0.8367 | 0.9696 | 0.9803 | 0.8749 |
| STARE | U-Net++ | DTI as released (0.5, 0.3) | 0.8530 | 0.8342 | 0.8726 | 0.8353 | 0.8954 | 25.8 | 21.1 | 15.7 | 0.9288 | 0.8364 | 0.9697 | 0.9805 | 0.8726 |
| STARE | U-Net++ | Dense CRF | 0.8496 | 0.8811 | 0.8203 | 0.7871 | 0.8839 | 49.2 | 44.5 | 18.4 | 0.9235 | 0.8340 | 0.9707 | 0.9876 | 0.8203 |
| STARE | U-Net++ | Closing 3 x 3 | 0.8500 | 0.8740 | 0.8272 | 0.7961 | 0.8837 | 46.5 | 41.8 | 21.3 | 0.9230 | 0.8340 | 0.9705 | 0.9866 | 0.8272 |
| STARE | U-Net++ | RGR | 0.8513 | 0.8648 | 0.8381 | 0.8249 | 0.8910 | 33.1 | 28.4 | 17.8 | 0.9287 | 0.8350 | 0.9705 | 0.9853 | 0.8381 |
| STARE | U-Net++ | RGR on the selected threshold | 0.8536 | 0.8470 | 0.8603 | 0.8399 | 0.8933 | 41.7 | 37.0 | 16.0 | 0.9313 | 0.8371 | 0.9702 | 0.9826 | 0.8603 |
| STARE | U-Net++ | Conservative-gate RGR | 0.8512 | 0.8744 | 0.8291 | 0.8053 | 0.8874 | 40.0 | 35.3 | 18.3 | 0.9263 | 0.8353 | 0.9708 | 0.9866 | 0.8291 |
| STARE | U-Net++ | RGR-P | 0.8511 | 0.8621 | 0.8403 | 0.8301 | 0.8918 | 19.5 | 14.8 | 17.4 | 0.9284 | 0.8347 | 0.9703 | 0.9849 | 0.8403 |
| STARE | U-Net++ | RGR-P, setting re-selected per run | 0.8510 | 0.8608 | 0.8414 | 0.8329 | 0.8918 | 13.3 | 8.8 | 16.4 | 0.9285 | 0.8346 | 0.9703 | 0.9847 | 0.8414 |
| STARE | U-Net++ | RGR-P, recall-oriented | 0.8494 | 0.8550 | 0.8439 | 0.8384 | 0.8891 | 8.5 | 6.2 | 14.4 | 0.9258 | 0.8327 | 0.9698 | 0.9839 | 0.8439 |
| FIVES | U-Net | Threshold 0.5 | 0.8332 | 0.8204 | 0.8464 | 0.7501 | 0.8277 | 390.4 | 386.4 | 17.6 | 0.8516 | 0.8154 | 0.9675 | 0.9803 | 0.8464 |
| FIVES | U-Net | Threshold selected on validation | 0.8235 | 0.7803 | 0.8717 | 0.7794 | 0.8194 | 458.6 | 454.6 | 18.4 | 0.8411 | 0.8052 | 0.9641 | 0.9740 | 0.8717 |
| FIVES | U-Net | Threshold 0.25 | 0.7930 | 0.7041 | 0.9075 | 0.8251 | 0.7945 | 588.9 | 584.8 | 17.9 | 0.8142 | 0.7757 | 0.9545 | 0.9595 | 0.9075 |
| FIVES | U-Net | Hysteresis 0.25 | 0.7974 | 0.7121 | 0.9059 | 0.8187 | 0.8111 | 192.8 | 188.7 | 18.1 | 0.8270 | 0.7801 | 0.9558 | 0.9611 | 0.9059 |
| FIVES | U-Net | DTI as described (0.5 to 0.3) | 0.8086 | 0.7379 | 0.8944 | 0.8044 | 0.8167 | 224.2 | 220.2 | 18.1 | 0.8334 | 0.7907 | 0.9594 | 0.9663 | 0.8944 |
| FIVES | U-Net | DTI as released (0.5, 0.3) | 0.8110 | 0.7448 | 0.8902 | 0.7934 | 0.8155 | 425.6 | 421.5 | 18.1 | 0.8319 | 0.7929 | 0.9602 | 0.9676 | 0.8902 |
| FIVES | U-Net | Closing 3 x 3 | 0.8334 | 0.8200 | 0.8471 | 0.7508 | 0.8280 | 378.9 | 374.8 | 19.8 | 0.8517 | 0.8155 | 0.9675 | 0.9803 | 0.8471 |
| FIVES | U-Net | RGR | 0.8239 | 0.7796 | 0.8737 | 0.7933 | 0.8117 | 327.9 | 323.9 | 21.6 | 0.8330 | 0.8057 | 0.9642 | 0.9738 | 0.8737 |
| FIVES | U-Net | RGR on the selected threshold | 0.8152 | 0.7537 | 0.8877 | 0.8061 | 0.8048 | 404.1 | 400.0 | 19.4 | 0.8253 | 0.7971 | 0.9614 | 0.9692 | 0.8877 |
| FIVES | U-Net | Conservative-gate RGR | 0.8255 | 0.7890 | 0.8655 | 0.7769 | 0.8134 | 339.8 | 335.8 | 20.1 | 0.8341 | 0.8071 | 0.9649 | 0.9754 | 0.8655 |
| FIVES | U-Net | RGR-P | 0.8225 | 0.7749 | 0.8763 | 0.8001 | 0.8060 | 186.7 | 182.6 | 31.3 | 0.8267 | 0.8042 | 0.9637 | 0.9730 | 0.8763 |
| FIVES | U-Net | RGR-P, setting re-selected per run | 0.8225 | 0.7749 | 0.8763 | 0.8001 | 0.8060 | 186.7 | 182.6 | 31.3 | 0.8267 | 0.8042 | 0.9637 | 0.9730 | 0.8763 |
| FIVES | U-Net | RGR-P, recall-oriented | 0.8192 | 0.7652 | 0.8815 | 0.8162 | 0.7878 | 136.2 | 132.2 | 67.8 | 0.8100 | 0.8010 | 0.9627 | 0.9713 | 0.8815 |
| FIVES | Attention U-Net | Threshold 0.5 | 0.8440 | 0.8265 | 0.8621 | 0.7710 | 0.8384 | 339.4 | 335.4 | 17.2 | 0.8585 | 0.8272 | 0.9694 | 0.9808 | 0.8621 |
| FIVES | Attention U-Net | Threshold selected on validation | 0.8356 | 0.7946 | 0.8812 | 0.7918 | 0.8307 | 389.9 | 385.8 | 16.8 | 0.8500 | 0.8185 | 0.9667 | 0.9758 | 0.8812 |
| FIVES | Attention U-Net | Threshold 0.25 | 0.8063 | 0.7219 | 0.9130 | 0.8305 | 0.8043 | 495.3 | 491.3 | 16.4 | 0.8219 | 0.7898 | 0.9579 | 0.9627 | 0.9130 |
| FIVES | Attention U-Net | Hysteresis 0.25 | 0.8098 | 0.7282 | 0.9119 | 0.8257 | 0.8196 | 154.8 | 150.8 | 16.4 | 0.8341 | 0.7933 | 0.9589 | 0.9639 | 0.9119 |
| FIVES | Attention U-Net | DTI as described (0.5 to 0.3) | 0.8202 | 0.7519 | 0.9021 | 0.8140 | 0.8255 | 184.8 | 180.8 | 16.9 | 0.8407 | 0.8033 | 0.9621 | 0.9684 | 0.9021 |
| FIVES | Attention U-Net | DTI as released (0.5, 0.3) | 0.8223 | 0.7576 | 0.8991 | 0.8061 | 0.8246 | 374.8 | 370.8 | 17.2 | 0.8395 | 0.8053 | 0.9627 | 0.9695 | 0.8991 |
| FIVES | Attention U-Net | Closing 3 x 3 | 0.8440 | 0.8261 | 0.8627 | 0.7715 | 0.8387 | 330.3 | 326.2 | 19.0 | 0.8585 | 0.8273 | 0.9694 | 0.9807 | 0.8627 |
| FIVES | Attention U-Net | RGR | 0.8351 | 0.7910 | 0.8842 | 0.8051 | 0.8228 | 295.3 | 291.3 | 18.1 | 0.8415 | 0.8180 | 0.9665 | 0.9752 | 0.8842 |
| FIVES | Attention U-Net | RGR on the selected threshold | 0.8277 | 0.7698 | 0.8950 | 0.8145 | 0.8166 | 349.8 | 345.7 | 16.6 | 0.8353 | 0.8108 | 0.9642 | 0.9716 | 0.8950 |
| FIVES | Attention U-Net | Conservative-gate RGR | 0.8373 | 0.8017 | 0.8763 | 0.7902 | 0.8262 | 306.1 | 302.1 | 18.1 | 0.8444 | 0.8202 | 0.9673 | 0.9770 | 0.8763 |
| FIVES | Attention U-Net | RGR-P | 0.8334 | 0.7866 | 0.8861 | 0.8100 | 0.8168 | 160.7 | 156.7 | 26.3 | 0.8354 | 0.8163 | 0.9660 | 0.9745 | 0.8861 |
| FIVES | Attention U-Net | RGR-P, setting re-selected per run | 0.8334 | 0.7866 | 0.8861 | 0.8100 | 0.8168 | 160.7 | 156.7 | 26.3 | 0.8354 | 0.8163 | 0.9660 | 0.9745 | 0.8861 |
| FIVES | Attention U-Net | RGR-P, recall-oriented | 0.8302 | 0.7778 | 0.8902 | 0.8221 | 0.7996 | 122.5 | 118.5 | 58.4 | 0.8198 | 0.8132 | 0.9651 | 0.9730 | 0.8902 |
| FIVES | U-Net++ | Threshold 0.5 | 0.8343 | 0.8463 | 0.8226 | 0.7089 | 0.8299 | 301.4 | 297.4 | 18.2 | 0.8530 | 0.8171 | 0.9686 | 0.9841 | 0.8226 |
| FIVES | U-Net++ | Threshold selected on validation | 0.8290 | 0.8085 | 0.8505 | 0.7420 | 0.8269 | 366.8 | 362.8 | 18.0 | 0.8473 | 0.8106 | 0.9663 | 0.9786 | 0.8505 |
| FIVES | U-Net++ | Threshold 0.25 | 0.8097 | 0.7462 | 0.8850 | 0.7865 | 0.8126 | 462.3 | 458.2 | 17.9 | 0.8307 | 0.7912 | 0.9601 | 0.9681 | 0.8850 |
| FIVES | U-Net++ | Hysteresis 0.25 | 0.8129 | 0.7531 | 0.8829 | 0.7783 | 0.8251 | 156.9 | 152.9 | 17.9 | 0.8394 | 0.7944 | 0.9610 | 0.9693 | 0.8829 |
| FIVES | U-Net++ | DTI as described (0.5 to 0.3) | 0.8202 | 0.7753 | 0.8707 | 0.7635 | 0.8274 | 182.9 | 178.8 | 18.4 | 0.8426 | 0.8016 | 0.9634 | 0.9732 | 0.8707 |
| FIVES | U-Net++ | DTI as released (0.5, 0.3) | 0.8217 | 0.7815 | 0.8661 | 0.7509 | 0.8241 | 354.6 | 350.5 | 18.4 | 0.8395 | 0.8030 | 0.9639 | 0.9743 | 0.8661 |
| FIVES | U-Net++ | Closing 3 x 3 | 0.8344 | 0.8460 | 0.8231 | 0.7094 | 0.8302 | 295.1 | 291.1 | 19.4 | 0.8528 | 0.8172 | 0.9687 | 0.9841 | 0.8231 |
| FIVES | U-Net++ | RGR | 0.8312 | 0.8118 | 0.8516 | 0.7544 | 0.8221 | 259.4 | 255.3 | 17.1 | 0.8424 | 0.8131 | 0.9668 | 0.9790 | 0.8516 |
| FIVES | U-Net++ | RGR on the selected threshold | 0.8248 | 0.7868 | 0.8667 | 0.7689 | 0.8185 | 331.6 | 327.6 | 17.7 | 0.8379 | 0.8064 | 0.9647 | 0.9751 | 0.8667 |
| FIVES | U-Net++ | Conservative-gate RGR | 0.8316 | 0.8221 | 0.8413 | 0.7354 | 0.8224 | 269.3 | 265.3 | 18.5 | 0.8426 | 0.8136 | 0.9673 | 0.9807 | 0.8413 |
| FIVES | U-Net++ | RGR-P | 0.8304 | 0.8084 | 0.8536 | 0.7601 | 0.8181 | 151.7 | 147.6 | 21.0 | 0.8376 | 0.8122 | 0.9665 | 0.9785 | 0.8536 |
| FIVES | U-Net++ | RGR-P, setting re-selected per run | 0.8301 | 0.8063 | 0.8553 | 0.7660 | 0.8142 | 127.7 | 123.7 | 28.6 | 0.8340 | 0.8119 | 0.9664 | 0.9782 | 0.8553 |
| FIVES | U-Net++ | RGR-P, recall-oriented | 0.8283 | 0.8001 | 0.8585 | 0.7752 | 0.8031 | 111.4 | 107.3 | 47.0 | 0.8243 | 0.8099 | 0.9658 | 0.9772 | 0.8585 |


**T_equal.** Values at the precision of the selected RGR setting; threshold, hysteresis and DTI values are interpolated along their test-set sweeps (retrospective).

| Dataset | Network | Procedure | Precision | TCR | Dice | clDice | Frag |
|---|---|---|---|---|---|---|---|
| DRIVE | U-Net | RGR | 0.8316 | 0.7060 | 0.8254 | 0.8291 | 61.0 |
| DRIVE | U-Net | Threshold | 0.8316 | 0.6995 | 0.8259 | 0.8287 | 75.1 |
| DRIVE | U-Net | Hysteresis | 0.8316 | 0.6990 | 0.8259 | 0.8289 | 64.2 |
| DRIVE | U-Net | DTI as released | 0.8316 | 0.6989 | 0.8259 | 0.8289 | 63.5 |
| DRIVE | Attention U-Net | RGR | 0.8330 | 0.7067 | 0.8263 | 0.8299 | 55.4 |
| DRIVE | Attention U-Net | Threshold | 0.8330 | 0.6997 | 0.8267 | 0.8291 | 67.1 |
| DRIVE | Attention U-Net | Hysteresis | 0.8330 | 0.6993 | 0.8267 | 0.8292 | 57.2 |
| DRIVE | Attention U-Net | DTI as released | 0.8330 | 0.6990 | 0.8266 | 0.8292 | 56.6 |
| DRIVE | U-Net++ | RGR | 0.8298 | 0.7113 | 0.8274 | 0.8304 | 45.5 |
| DRIVE | U-Net++ | Threshold | 0.8298 | 0.7044 | 0.8276 | 0.8300 | 55.1 |
| DRIVE | U-Net++ | Hysteresis | 0.8298 | 0.7041 | 0.8276 | 0.8301 | 46.4 |
| DRIVE | U-Net++ | DTI as released | 0.8298 | 0.7040 | 0.8276 | 0.8302 | 45.8 |
| CHASE_DB1 | U-Net | RGR | 0.7443 | 0.7388 | 0.8021 | 0.8413 | 48.9 |
| CHASE_DB1 | U-Net | Threshold | 0.7443 | 0.7329 | 0.8030 | 0.8429 | 82.1 |
| CHASE_DB1 | U-Net | Hysteresis | 0.7443 | 0.7315 | 0.8031 | 0.8450 | 48.0 |
| CHASE_DB1 | U-Net | DTI as released | 0.7443 | 0.7283 | 0.8028 | 0.8452 | 54.5 |
| CHASE_DB1 | Attention U-Net | RGR | 0.7532 | 0.7230 | 0.8041 | 0.8406 | 51.2 |
| CHASE_DB1 | Attention U-Net | Threshold | 0.7532 | 0.7203 | 0.8063 | 0.8420 | 85.9 |
| CHASE_DB1 | Attention U-Net | Hysteresis | 0.7532 | 0.7183 | 0.8062 | 0.8440 | 49.6 |
| CHASE_DB1 | Attention U-Net | DTI as released | 0.7532 | 0.7155 | 0.8060 | 0.8447 | 51.9 |
| CHASE_DB1 | U-Net++ | RGR | 0.7525 | 0.7387 | 0.8045 | 0.8399 | 49.0 |
| CHASE_DB1 | U-Net++ | Threshold | 0.7525 | 0.7372 | 0.8064 | 0.8420 | 77.5 |
| CHASE_DB1 | U-Net++ | Hysteresis | 0.7525 | 0.7347 | 0.8063 | 0.8436 | 45.9 |
| CHASE_DB1 | U-Net++ | DTI as released | 0.7525 | 0.7319 | 0.8061 | 0.8445 | 48.2 |
| STARE | U-Net | RGR | 0.8608 | 0.8118 | 0.8442 | 0.8855 | 47.0 |
| STARE | U-Net | Threshold | 0.8608 | 0.7937 | 0.8449 | 0.8814 | 67.1 |
| STARE | U-Net | Hysteresis | 0.8608 | 0.7928 | 0.8449 | 0.8816 | 51.4 |
| STARE | U-Net | DTI as released | 0.8608 | 0.7922 | 0.8448 | 0.8815 | 51.8 |
| STARE | Attention U-Net | RGR | 0.8564 | 0.8229 | 0.8480 | 0.8887 | 42.9 |
| STARE | Attention U-Net | Threshold | 0.8564 | 0.8070 | 0.8493 | 0.8859 | 63.5 |
| STARE | Attention U-Net | Hysteresis | 0.8564 | 0.8061 | 0.8493 | 0.8861 | 47.0 |
| STARE | Attention U-Net | DTI as released | 0.8564 | 0.8058 | 0.8493 | 0.8863 | 46.8 |
| STARE | U-Net++ | RGR | 0.8648 | 0.8249 | 0.8513 | 0.8910 | 33.1 |
| STARE | U-Net++ | Threshold | 0.8648 | 0.8105 | 0.8526 | 0.8886 | 54.8 |
| STARE | U-Net++ | Hysteresis | 0.8648 | 0.8093 | 0.8526 | 0.8888 | 37.5 |
| STARE | U-Net++ | DTI as released | 0.8648 | 0.8084 | 0.8525 | 0.8886 | 37.6 |
| FIVES | U-Net | RGR | 0.7796 | 0.7933 | 0.8239 | 0.8117 | 327.9 |
| FIVES | U-Net | Threshold | 0.7796 | 0.7799 | 0.8233 | 0.8192 | 459.9 |
| FIVES | U-Net | Hysteresis | 0.7796 | 0.7789 | 0.8234 | 0.8236 | 288.9 |
| FIVES | U-Net | DTI as released | 0.7796 | 0.7761 | 0.8233 | 0.8227 | 392.7 |
| FIVES | Attention U-Net | RGR | 0.7910 | 0.8051 | 0.8351 | 0.8228 | 295.3 |
| FIVES | Attention U-Net | Threshold | 0.7910 | 0.7940 | 0.8345 | 0.8298 | 395.1 |
| FIVES | Attention U-Net | Hysteresis | 0.7910 | 0.7932 | 0.8346 | 0.8335 | 250.0 |
| FIVES | Attention U-Net | DTI as released | 0.7910 | 0.7913 | 0.8345 | 0.8328 | 346.2 |
| FIVES | U-Net++ | RGR | 0.8118 | 0.7544 | 0.8312 | 0.8221 | 259.4 |
| FIVES | U-Net++ | Threshold | 0.8118 | 0.7394 | 0.8296 | 0.8276 | 359.6 |
| FIVES | U-Net++ | Hysteresis | 0.8118 | 0.7376 | 0.8297 | 0.8304 | 235.1 |
| FIVES | U-Net++ | DTI as released | 0.8118 | 0.7342 | 0.8296 | 0.8290 | 318.7 |


**T_bridges.** Reconnection analysis of bridges (added components joining two or more seed fragments), pooled over the three networks (seed 7).

| Dataset | Variant | Context | Bridges | Correct | Correct (%) | Shortcut | Offset | Unannotated | Unannotated on observer-2 vessel |
|---|---|---|---|---|---|---|---|---|---|
| DRIVE | RGR | all bridges | 742 | 604 | 81.4 | 2 | 6 | 130 | - |
| DRIVE | RGR | near a junction or crossing | 203 | 202 | 99.5 | 0 | 1 | 0 | - |
| DRIVE | RGR | closely adjacent vessels | 45 | 38 | 84.4 | 2 | 0 | 5 | - |
| DRIVE | RGR | optic-disc region | 91 | 62 | 68.1 | 0 | 0 | 29 | - |
| DRIVE | RGR | none of these | 448 | 346 | 77.2 | 0 | 5 | 97 | - |
| DRIVE | Conservative-gate RGR | all bridges | 594 | 489 | 82.3 | 0 | 6 | 99 | - |
| DRIVE | Conservative-gate RGR | near a junction or crossing | 130 | 130 | 100.0 | 0 | 0 | 0 | - |
| DRIVE | Conservative-gate RGR | closely adjacent vessels | 33 | 30 | 90.9 | 0 | 0 | 3 | - |
| DRIVE | Conservative-gate RGR | optic-disc region | 60 | 41 | 68.3 | 0 | 0 | 19 | - |
| DRIVE | Conservative-gate RGR | none of these | 401 | 317 | 79.1 | 0 | 6 | 78 | - |
| DRIVE | RGR-P | all bridges | 2596 | 2042 | 78.7 | 33 | 30 | 491 | - |
| DRIVE | RGR-P | near a junction or crossing | 1050 | 998 | 95.0 | 3 | 8 | 41 | - |
| DRIVE | RGR-P | closely adjacent vessels | 197 | 136 | 69.0 | 33 | 3 | 25 | - |
| DRIVE | RGR-P | optic-disc region | 246 | 150 | 61.0 | 12 | 4 | 80 | - |
| DRIVE | RGR-P | none of these | 1290 | 907 | 70.3 | 0 | 18 | 365 | - |
| DRIVE | RGR-P, setting re-selected per run | all bridges | 2698 | 2103 | 77.9 | 47 | 30 | 518 | - |
| DRIVE | RGR-P, setting re-selected per run | near a junction or crossing | 1111 | 1050 | 94.5 | 5 | 8 | 48 | - |
| DRIVE | RGR-P, setting re-selected per run | closely adjacent vessels | 216 | 140 | 64.8 | 47 | 3 | 26 | - |
| DRIVE | RGR-P, setting re-selected per run | optic-disc region | 266 | 155 | 58.3 | 16 | 4 | 91 | - |
| DRIVE | RGR-P, setting re-selected per run | none of these | 1310 | 915 | 69.8 | 0 | 18 | 377 | - |
| DRIVE | RGR-P, recall-oriented | all bridges | 3014 | 2174 | 72.1 | 189 | 40 | 611 | - |
| DRIVE | RGR-P, recall-oriented | near a junction or crossing | 1313 | 1203 | 91.6 | 28 | 13 | 69 | - |
| DRIVE | RGR-P, recall-oriented | closely adjacent vessels | 435 | 191 | 43.9 | 189 | 10 | 45 | - |
| DRIVE | RGR-P, recall-oriented | optic-disc region | 329 | 162 | 49.2 | 49 | 5 | 113 | - |
| DRIVE | RGR-P, recall-oriented | none of these | 1260 | 820 | 65.1 | 0 | 20 | 420 | - |
| CHASE_DB1 | RGR | all bridges | 455 | 341 | 74.9 | 2 | 9 | 103 | 26/103 |
| CHASE_DB1 | RGR | near a junction or crossing | 118 | 115 | 97.5 | 0 | 1 | 2 | 2/2 |
| CHASE_DB1 | RGR | closely adjacent vessels | 31 | 20 | 64.5 | 2 | 0 | 9 | 5/9 |
| CHASE_DB1 | RGR | optic-disc region | 92 | 63 | 68.5 | 1 | 3 | 25 | 4/25 |
| CHASE_DB1 | RGR | none of these | 262 | 182 | 69.5 | 0 | 5 | 75 | 20/75 |
| CHASE_DB1 | Conservative-gate RGR | all bridges | 300 | 214 | 71.3 | 2 | 4 | 80 | 20/80 |
| CHASE_DB1 | Conservative-gate RGR | near a junction or crossing | 59 | 57 | 96.6 | 0 | 1 | 1 | 1/1 |
| CHASE_DB1 | Conservative-gate RGR | closely adjacent vessels | 13 | 9 | 69.2 | 2 | 0 | 2 | 1/2 |
| CHASE_DB1 | Conservative-gate RGR | optic-disc region | 58 | 38 | 65.5 | 1 | 3 | 16 | 2/16 |
| CHASE_DB1 | Conservative-gate RGR | none of these | 195 | 132 | 67.7 | 0 | 0 | 63 | 17/63 |
| CHASE_DB1 | RGR-P | all bridges | 797 | 566 | 71.0 | 13 | 12 | 206 | 62/206 |
| CHASE_DB1 | RGR-P | near a junction or crossing | 215 | 208 | 96.7 | 2 | 2 | 3 | 3/3 |
| CHASE_DB1 | RGR-P | closely adjacent vessels | 61 | 30 | 49.2 | 13 | 1 | 17 | 6/17 |
| CHASE_DB1 | RGR-P | optic-disc region | 140 | 93 | 66.4 | 2 | 5 | 40 | 6/40 |
| CHASE_DB1 | RGR-P | none of these | 469 | 308 | 65.7 | 0 | 5 | 156 | 52/156 |
| CHASE_DB1 | RGR-P, setting re-selected per run | all bridges | 877 | 604 | 68.9 | 26 | 14 | 233 | 71/233 |
| CHASE_DB1 | RGR-P, setting re-selected per run | near a junction or crossing | 252 | 236 | 93.7 | 6 | 4 | 6 | 5/6 |
| CHASE_DB1 | RGR-P, setting re-selected per run | closely adjacent vessels | 79 | 29 | 36.7 | 26 | 1 | 23 | 8/23 |
| CHASE_DB1 | RGR-P, setting re-selected per run | optic-disc region | 152 | 96 | 63.2 | 5 | 7 | 44 | 9/44 |
| CHASE_DB1 | RGR-P, setting re-selected per run | none of these | 496 | 318 | 64.1 | 0 | 4 | 174 | 56/174 |
| CHASE_DB1 | RGR-P, recall-oriented | all bridges | 1126 | 721 | 64.0 | 78 | 22 | 305 | 74/305 |
| CHASE_DB1 | RGR-P, recall-oriented | near a junction or crossing | 352 | 327 | 92.9 | 8 | 6 | 11 | 7/11 |
| CHASE_DB1 | RGR-P, recall-oriented | closely adjacent vessels | 166 | 52 | 31.3 | 78 | 5 | 31 | 6/31 |
| CHASE_DB1 | RGR-P, recall-oriented | optic-disc region | 198 | 119 | 60.1 | 18 | 9 | 52 | 9/52 |
| CHASE_DB1 | RGR-P, recall-oriented | none of these | 563 | 327 | 58.1 | 0 | 6 | 230 | 59/230 |
| STARE | RGR | all bridges | 621 | 526 | 84.7 | 2 | 1 | 92 | 85/92 |
| STARE | RGR | near a junction or crossing | 181 | 180 | 99.4 | 1 | 0 | 0 | - |
| STARE | RGR | closely adjacent vessels | 33 | 28 | 84.8 | 2 | 0 | 3 | 3/3 |
| STARE | RGR | optic-disc region | 46 | 36 | 78.3 | 1 | 0 | 9 | 8/9 |
| STARE | RGR | images with pathology | 46 | 32 | 69.6 | 0 | 0 | 14 | 8/14 |
| STARE | RGR | none of these | 386 | 305 | 79.0 | 0 | 1 | 80 | 74/80 |
| STARE | Conservative-gate RGR | all bridges | 382 | 328 | 85.9 | 0 | 0 | 54 | 49/54 |
| STARE | Conservative-gate RGR | near a junction or crossing | 89 | 89 | 100.0 | 0 | 0 | 0 | - |
| STARE | Conservative-gate RGR | closely adjacent vessels | 13 | 11 | 84.6 | 0 | 0 | 2 | 2/2 |
| STARE | Conservative-gate RGR | optic-disc region | 24 | 19 | 79.2 | 0 | 0 | 5 | 5/5 |
| STARE | Conservative-gate RGR | images with pathology | 40 | 27 | 67.5 | 0 | 0 | 13 | 8/13 |
| STARE | Conservative-gate RGR | none of these | 265 | 218 | 82.3 | 0 | 0 | 47 | 42/47 |
| STARE | RGR-P | all bridges | 1101 | 860 | 78.1 | 11 | 6 | 224 | 198/224 |
| STARE | RGR-P | near a junction or crossing | 367 | 355 | 96.7 | 4 | 2 | 6 | 6/6 |
| STARE | RGR-P | closely adjacent vessels | 47 | 33 | 70.2 | 11 | 0 | 3 | 3/3 |
| STARE | RGR-P | optic-disc region | 92 | 72 | 78.3 | 4 | 0 | 16 | 15/16 |
| STARE | RGR-P | images with pathology | 196 | 140 | 71.4 | 0 | 1 | 55 | 44/55 |
| STARE | RGR-P | none of these | 656 | 452 | 68.9 | 0 | 4 | 200 | 175/200 |
| STARE | RGR-P, setting re-selected per run | all bridges | 1163 | 899 | 77.3 | 16 | 6 | 242 | 212/242 |
| STARE | RGR-P, setting re-selected per run | near a junction or crossing | 405 | 393 | 97.0 | 4 | 2 | 6 | 6/6 |
| STARE | RGR-P, setting re-selected per run | closely adjacent vessels | 56 | 37 | 66.1 | 16 | 0 | 3 | 3/3 |
| STARE | RGR-P, setting re-selected per run | optic-disc region | 100 | 76 | 76.0 | 6 | 0 | 18 | 17/18 |
| STARE | RGR-P, setting re-selected per run | images with pathology | 209 | 147 | 70.3 | 1 | 1 | 60 | 46/60 |
| STARE | RGR-P, setting re-selected per run | none of these | 673 | 453 | 67.3 | 0 | 4 | 216 | 187/216 |
| STARE | RGR-P, recall-oriented | all bridges | 1373 | 976 | 71.1 | 74 | 8 | 315 | 257/315 |
| STARE | RGR-P, recall-oriented | near a junction or crossing | 523 | 505 | 96.6 | 3 | 3 | 12 | 11/12 |
| STARE | RGR-P, recall-oriented | closely adjacent vessels | 150 | 60 | 40.0 | 74 | 3 | 13 | 11/13 |
| STARE | RGR-P, recall-oriented | optic-disc region | 123 | 84 | 68.3 | 17 | 0 | 22 | 20/22 |
| STARE | RGR-P, recall-oriented | images with pathology | 268 | 167 | 62.3 | 17 | 0 | 84 | 58/84 |
| STARE | RGR-P, recall-oriented | none of these | 684 | 409 | 59.8 | 0 | 3 | 272 | 218/272 |
| FIVES | RGR | all bridges | 4563 | 2208 | 48.4 | 16 | 110 | 2229 | - |
| FIVES | RGR | near a junction or crossing | 1223 | 1031 | 84.3 | 3 | 24 | 165 | - |
| FIVES | RGR | closely adjacent vessels | 430 | 217 | 50.5 | 16 | 18 | 179 | - |
| FIVES | RGR | optic-disc region | 798 | 422 | 52.9 | 9 | 23 | 344 | - |
| FIVES | RGR | images with pathology | 2949 | 1671 | 56.7 | 8 | 50 | 1220 | - |
| FIVES | RGR | none of these | 2716 | 923 | 34.0 | 0 | 63 | 1730 | - |
| FIVES | Conservative-gate RGR | all bridges | 3778 | 1795 | 47.5 | 10 | 74 | 1899 | - |
| FIVES | Conservative-gate RGR | near a junction or crossing | 801 | 690 | 86.1 | 3 | 15 | 93 | - |
| FIVES | Conservative-gate RGR | closely adjacent vessels | 269 | 147 | 54.6 | 10 | 8 | 104 | - |
| FIVES | Conservative-gate RGR | optic-disc region | 669 | 357 | 53.4 | 3 | 16 | 293 | - |
| FIVES | Conservative-gate RGR | images with pathology | 2374 | 1319 | 55.6 | 3 | 37 | 1015 | - |
| FIVES | Conservative-gate RGR | none of these | 2422 | 866 | 35.8 | 0 | 43 | 1513 | - |
| FIVES | RGR-P | all bridges | 14212 | 4384 | 30.8 | 112 | 236 | 9480 | - |
| FIVES | RGR-P | near a junction or crossing | 2499 | 1990 | 79.6 | 26 | 47 | 436 | - |
| FIVES | RGR-P | closely adjacent vessels | 845 | 344 | 40.7 | 112 | 36 | 353 | - |
| FIVES | RGR-P | optic-disc region | 1228 | 616 | 50.2 | 59 | 48 | 505 | - |
| FIVES | RGR-P | images with pathology | 10282 | 3186 | 31.0 | 63 | 126 | 6907 | - |
| FIVES | RGR-P | none of these | 10662 | 2036 | 19.1 | 0 | 138 | 8488 | - |
| FIVES | RGR-P, setting re-selected per run | all bridges | 14771 | 4573 | 31.0 | 168 | 232 | 9798 | - |
| FIVES | RGR-P, setting re-selected per run | near a junction or crossing | 2724 | 2148 | 78.9 | 41 | 49 | 486 | - |
| FIVES | RGR-P, setting re-selected per run | closely adjacent vessels | 938 | 352 | 37.5 | 168 | 39 | 379 | - |
| FIVES | RGR-P, setting re-selected per run | optic-disc region | 1267 | 623 | 49.2 | 80 | 46 | 518 | - |
| FIVES | RGR-P, setting re-selected per run | images with pathology | 10704 | 3332 | 31.1 | 97 | 122 | 7153 | - |
| FIVES | RGR-P, setting re-selected per run | none of these | 10943 | 2067 | 18.9 | 0 | 133 | 8743 | - |
| FIVES | RGR-P, recall-oriented | all bridges | 17132 | 4993 | 29.1 | 632 | 209 | 11298 | - |
| FIVES | RGR-P, recall-oriented | near a junction or crossing | 3823 | 2654 | 69.4 | 189 | 55 | 925 | - |
| FIVES | RGR-P, recall-oriented | closely adjacent vessels | 1855 | 521 | 28.1 | 632 | 52 | 650 | - |
| FIVES | RGR-P, recall-oriented | optic-disc region | 1477 | 653 | 44.2 | 183 | 40 | 601 | - |
| FIVES | RGR-P, recall-oriented | images with pathology | 12472 | 3670 | 29.4 | 443 | 114 | 8245 | - |
| FIVES | RGR-P, recall-oriented | none of these | 11775 | 1971 | 16.7 | 0 | 107 | 9697 | - |


**T_dicerule.** The reference-free Dice rule (Eqs. S5 and S6) evaluated prospectively: the direction of the Dice change predicted from the probabilities against the observed direction, per image.

| Dataset | Network | Variant | Images | Direction right | Predicted rise | Observed rise | Largest Dice error when wrong (pp) | Bias of est. Dice (pp) | Bias of est. precision (pp) |
|---|---|---|---|---|---|---|---|---|---|
| DRIVE | U-Net | RGR | 20 | 10 | 0 | 10 | 0.38 | +4.6 | -3.4 |
| DRIVE | U-Net | Conservative-gate RGR | 20 | 12 | 20 | 12 | 0.11 | +4.6 | -0.5 |
| DRIVE | Attention U-Net | RGR | 20 | 11 | 0 | 9 | 0.41 | +4.6 | -2.8 |
| DRIVE | Attention U-Net | Conservative-gate RGR | 20 | 12 | 20 | 12 | 0.11 | +4.6 | +0.2 |
| DRIVE | U-Net++ | RGR | 20 | 10 | 0 | 10 | 0.30 | +4.8 | -2.6 |
| DRIVE | U-Net++ | Conservative-gate RGR | 20 | 12 | 20 | 12 | 0.11 | +4.8 | +0.2 |
| CHASE_DB1 | U-Net | RGR | 8 | 8 | 0 | 0 | - | +6.5 | +5.1 |
| CHASE_DB1 | U-Net | Conservative-gate RGR | 8 | 2 | 8 | 2 | 0.43 | +6.5 | +8.6 |
| CHASE_DB1 | Attention U-Net | RGR | 8 | 7 | 0 | 1 | 0.15 | +6.6 | +4.0 |
| CHASE_DB1 | Attention U-Net | Conservative-gate RGR | 8 | 2 | 8 | 2 | 0.27 | +6.6 | +7.0 |
| CHASE_DB1 | U-Net++ | RGR | 8 | 7 | 0 | 1 | 0.20 | +6.5 | +3.6 |
| CHASE_DB1 | U-Net++ | Conservative-gate RGR | 8 | 3 | 8 | 3 | 0.29 | +6.5 | +6.5 |
| STARE | U-Net | RGR | 10 | 3 | 0 | 7 | 0.91 | +4.6 | -10.3 |
| STARE | U-Net | Conservative-gate RGR | 10 | 8 | 10 | 8 | 0.07 | +4.6 | -8.3 |
| STARE | Attention U-Net | RGR | 10 | 5 | 0 | 5 | 0.79 | +4.5 | -3.4 |
| STARE | Attention U-Net | Conservative-gate RGR | 10 | 6 | 10 | 6 | 0.23 | +4.5 | +0.2 |
| STARE | U-Net++ | RGR | 10 | 3 | 0 | 7 | 0.75 | +4.6 | -8.6 |
| STARE | U-Net++ | Conservative-gate RGR | 10 | 8 | 10 | 8 | 0.17 | +4.6 | -6.6 |
| FIVES | U-Net | RGR | 40 | 28 | 7 | 9 | 4.83 | +0.3 | +3.4 |
| FIVES | U-Net | Conservative-gate RGR | 40 | 13 | 40 | 13 | 6.81 | +0.3 | +4.9 |
| FIVES | Attention U-Net | RGR | 40 | 33 | 4 | 5 | 6.30 | +0.7 | +4.5 |
| FIVES | Attention U-Net | Conservative-gate RGR | 40 | 12 | 40 | 12 | 9.29 | +0.7 | +6.4 |
| FIVES | U-Net++ | RGR | 40 | 20 | 5 | 17 | 3.70 | +1.8 | -3.6 |
| FIVES | U-Net++ | Conservative-gate RGR | 40 | 25 | 40 | 25 | 3.90 | +1.8 | -1.9 |


**T_gate.** Gate chosen by the conservative-gate rule per image against the gate that maximises the true Dice of that image (gates 0.45 to 0.15 or no addition).

| Dataset | Network | Images | Chosen = optimum | Within one step | Dice rose | Dice fell | Mean Dice left on the table (pp) | Mean Dice gain of the optimum (pp) |
|---|---|---|---|---|---|---|---|---|
| DRIVE | U-Net | 20 | 2 | 3 | 12 | 8 | 0.05 | 0.09 |
| DRIVE | Attention U-Net | 20 | 1 | 6 | 12 | 8 | 0.04 | 0.08 |
| DRIVE | U-Net++ | 20 | 1 | 4 | 12 | 8 | 0.05 | 0.07 |
| CHASE_DB1 | U-Net | 8 | 0 | 3 | 2 | 6 | 0.17 | 0.03 |
| CHASE_DB1 | Attention U-Net | 8 | 2 | 3 | 2 | 6 | 0.14 | 0.06 |
| CHASE_DB1 | U-Net++ | 8 | 3 | 3 | 3 | 5 | 0.13 | 0.06 |
| STARE | U-Net | 10 | 1 | 3 | 8 | 2 | 0.15 | 0.30 |
| STARE | Attention U-Net | 10 | 1 | 2 | 6 | 4 | 0.14 | 0.21 |
| STARE | U-Net++ | 10 | 1 | 3 | 8 | 2 | 0.14 | 0.25 |
| FIVES | U-Net | 40 | 5 | 13 | 13 | 27 | 0.78 | 0.47 |
| FIVES | Attention U-Net | 40 | 3 | 11 | 12 | 28 | 0.65 | 0.24 |
| FIVES | U-Net++ | 40 | 7 | 13 | 25 | 15 | 0.46 | 0.66 |


**T_measure.** Downstream measurements: mean signed error against the reference over test images (mean absolute error in brackets). Branch and end points after removing spurs of at most 5 DRIVE-equivalent pixels.

| Dataset | Network | Mask | Density (pp) | Centreline length (%) | Branch points (%) | End points (%) | Fractal dimension |
|---|---|---|---|---|---|---|---|
| DRIVE | U-Net | Threshold 0.5 | -0.4 (1.2) | -19.1 (19.1) | -35.4 (35.4) | +73.4 (73.4) | -0.055 (0.055) |
| DRIVE | U-Net | RGR | -0.2 (1.1) | -17.0 (17.1) | -30.0 (31.0) | +72.0 (72.0) | -0.049 (0.049) |
| DRIVE | U-Net | Conservative-gate RGR | -0.3 (1.1) | -17.9 (17.9) | -33.1 (33.4) | +74.4 (74.4) | -0.052 (0.052) |
| DRIVE | U-Net | Hysteresis 0.25 | +1.9 (2.0) | -13.4 (14.2) | -23.5 (26.4) | +20.4 (24.6) | -0.040 (0.042) |
| DRIVE | Attention U-Net | Threshold 0.5 | -0.4 (1.2) | -18.9 (18.9) | -33.2 (33.8) | +61.3 (61.3) | -0.054 (0.054) |
| DRIVE | Attention U-Net | RGR | -0.2 (1.1) | -16.9 (17.0) | -27.8 (29.0) | +59.4 (59.4) | -0.048 (0.048) |
| DRIVE | Attention U-Net | Conservative-gate RGR | -0.3 (1.1) | -17.8 (17.8) | -30.9 (31.7) | +62.0 (62.0) | -0.051 (0.051) |
| DRIVE | Attention U-Net | Hysteresis 0.25 | +2.0 (2.0) | -13.0 (13.7) | -21.3 (25.4) | +11.4 (18.4) | -0.039 (0.040) |
| DRIVE | U-Net++ | Threshold 0.5 | -0.3 (1.1) | -18.0 (18.0) | -33.0 (33.6) | +49.8 (49.8) | -0.051 (0.051) |
| DRIVE | U-Net++ | RGR | -0.1 (1.1) | -16.0 (16.3) | -27.4 (29.6) | +47.9 (47.9) | -0.045 (0.046) |
| DRIVE | U-Net++ | Conservative-gate RGR | -0.2 (1.1) | -17.0 (17.1) | -30.9 (32.0) | +50.7 (50.7) | -0.048 (0.048) |
| DRIVE | U-Net++ | Hysteresis 0.25 | +2.0 (2.0) | -12.4 (13.4) | -19.0 (24.4) | +9.0 (18.4) | -0.037 (0.038) |
| CHASE_DB1 | U-Net | Threshold 0.5 | +0.7 (0.7) | -14.0 (14.0) | -24.2 (24.2) | +207.7 (207.7) | -0.041 (0.041) |
| CHASE_DB1 | U-Net | RGR | +1.5 (1.5) | -7.2 (7.7) | +28.7 (29.2) | +153.4 (153.4) | -0.024 (0.024) |
| CHASE_DB1 | U-Net | Conservative-gate RGR | +1.1 (1.1) | -11.4 (11.4) | -8.6 (17.0) | +185.7 (185.7) | -0.035 (0.035) |
| CHASE_DB1 | U-Net | Hysteresis 0.25 | +2.4 (2.4) | -7.8 (8.1) | +0.2 (8.6) | +118.3 (118.3) | -0.029 (0.029) |
| CHASE_DB1 | Attention U-Net | Threshold 0.5 | +0.5 (0.6) | -15.3 (15.3) | -24.1 (24.1) | +218.5 (218.5) | -0.042 (0.042) |
| CHASE_DB1 | Attention U-Net | RGR | +1.3 (1.3) | -8.7 (9.4) | +22.4 (29.5) | +161.1 (161.1) | -0.025 (0.025) |
| CHASE_DB1 | Attention U-Net | Conservative-gate RGR | +0.8 (0.8) | -12.7 (12.7) | -12.5 (15.4) | +198.9 (198.9) | -0.035 (0.035) |
| CHASE_DB1 | Attention U-Net | Hysteresis 0.25 | +2.2 (2.2) | -9.0 (9.2) | -4.4 (15.2) | +120.7 (120.7) | -0.029 (0.029) |
| CHASE_DB1 | U-Net++ | Threshold 0.5 | +0.5 (0.6) | -13.0 (13.0) | -24.4 (24.4) | +211.3 (211.3) | -0.038 (0.038) |
| CHASE_DB1 | U-Net++ | RGR | +1.4 (1.4) | -6.6 (7.1) | +25.1 (25.1) | +161.2 (161.2) | -0.020 (0.020) |
| CHASE_DB1 | U-Net++ | Conservative-gate RGR | +0.9 (0.9) | -10.4 (10.4) | -8.9 (11.3) | +185.8 (185.8) | -0.031 (0.031) |
| CHASE_DB1 | U-Net++ | Hysteresis 0.25 | +2.2 (2.2) | -7.0 (7.5) | -0.3 (6.9) | +118.6 (118.6) | -0.025 (0.025) |
| STARE | U-Net | Threshold 0.5 | -0.7 (0.9) | -13.1 (13.1) | -27.2 (27.2) | +118.5 (118.5) | -0.039 (0.039) |
| STARE | U-Net | RGR | -0.4 (0.9) | -9.9 (10.1) | -20.2 (20.6) | +101.6 (101.6) | -0.031 (0.031) |
| STARE | U-Net | Conservative-gate RGR | -0.6 (0.9) | -11.7 (11.7) | -23.9 (23.9) | +117.5 (117.5) | -0.035 (0.035) |
| STARE | U-Net | Hysteresis 0.25 | +0.9 (1.2) | -7.1 (8.6) | -11.1 (14.0) | +51.6 (57.2) | -0.026 (0.026) |
| STARE | Attention U-Net | Threshold 0.5 | -0.5 (0.8) | -11.1 (11.1) | -24.4 (24.4) | +104.7 (104.7) | -0.034 (0.034) |
| STARE | Attention U-Net | RGR | -0.2 (0.8) | -8.2 (8.4) | -17.2 (17.2) | +89.0 (89.1) | -0.028 (0.028) |
| STARE | Attention U-Net | Conservative-gate RGR | -0.4 (0.8) | -10.0 (10.0) | -21.9 (21.9) | +102.5 (102.5) | -0.032 (0.032) |
| STARE | Attention U-Net | Hysteresis 0.25 | +1.0 (1.2) | -5.8 (7.5) | -13.2 (15.0) | +49.0 (51.7) | -0.023 (0.023) |
| STARE | U-Net++ | Threshold 0.5 | -0.6 (0.9) | -10.7 (10.7) | -23.4 (23.4) | +77.5 (77.5) | -0.032 (0.032) |
| STARE | U-Net++ | RGR | -0.3 (0.8) | -7.7 (8.1) | -16.2 (16.2) | +63.9 (63.9) | -0.025 (0.025) |
| STARE | U-Net++ | Conservative-gate RGR | -0.5 (0.8) | -9.4 (9.4) | -19.6 (19.6) | +74.9 (74.9) | -0.030 (0.030) |
| STARE | U-Net++ | Hysteresis 0.25 | +0.9 (1.0) | -5.0 (7.0) | -10.0 (11.2) | +40.3 (45.0) | -0.019 (0.019) |
| FIVES | U-Net | Threshold 0.5 | +0.3 (1.1) | +0.5 (16.0) | +15.1 (43.7) | +1162.7 (1162.7) | -0.067 (0.067) |
| FIVES | U-Net | RGR | +1.2 (1.4) | +22.2 (25.6) | +154.7 (154.7) | +870.6 (870.6) | -0.031 (0.037) |
| FIVES | U-Net | Conservative-gate RGR | +0.9 (1.3) | +19.7 (26.3) | +121.2 (122.4) | +913.4 (913.4) | -0.039 (0.042) |
| FIVES | U-Net | Hysteresis 0.25 | +2.6 (2.7) | +21.1 (24.1) | +61.4 (66.8) | +817.8 (817.8) | -0.036 (0.040) |
| FIVES | Attention U-Net | Threshold 0.5 | +0.4 (0.9) | +1.6 (14.2) | +1.4 (36.0) | +988.8 (988.8) | -0.060 (0.060) |
| FIVES | Attention U-Net | RGR | +1.1 (1.3) | +19.9 (23.6) | +120.8 (120.8) | +780.5 (780.5) | -0.030 (0.035) |
| FIVES | Attention U-Net | Conservative-gate RGR | +0.9 (1.2) | +16.7 (22.9) | +80.9 (87.2) | +828.3 (828.3) | -0.039 (0.040) |
| FIVES | Attention U-Net | Hysteresis 0.25 | +2.4 (2.5) | +19.8 (22.6) | +39.1 (52.4) | +695.1 (695.1) | -0.035 (0.037) |
| FIVES | U-Net++ | Threshold 0.5 | -0.3 (1.1) | -9.3 (17.2) | -10.4 (39.0) | +872.4 (872.4) | -0.063 (0.063) |
| FIVES | U-Net++ | RGR | +0.5 (1.2) | +8.5 (18.9) | +101.1 (103.3) | +689.1 (689.1) | -0.031 (0.036) |
| FIVES | U-Net++ | Conservative-gate RGR | +0.2 (1.1) | +4.8 (20.5) | +66.6 (75.6) | +719.7 (719.7) | -0.040 (0.042) |
| FIVES | U-Net++ | Hysteresis 0.25 | +1.6 (1.9) | +7.3 (17.9) | +21.4 (47.5) | +729.0 (729.0) | -0.036 (0.039) |


**T_boot.** Change relative to the 0.5 threshold with bootstrap 95% percentile intervals over images (10,000 resamples) and two-sided Wilcoxon p-values; Holm adjustment over the dataset-network tests of each procedure and measure.

| Dataset | Network | Procedure | dTCR (pp) [95% CI] | dDice (pp) [95% CI] | dPrecision (pp) [95% CI] | dFrag [95% CI] | p TCR (raw / Holm) | p Dice (raw / Holm) |
|---|---|---|---|---|---|---|---|---|
| DRIVE | U-Net | RGR | +1.62 [+1.11, +2.25] | +0.01 [-0.07, +0.09] | -0.70 [-0.94, -0.49] | -14.3 [-19.4, -10.0] | 1.9e-06 / 1.7e-05 | 0.84 / 1 |
| DRIVE | U-Net | Conservative-gate RGR | +0.96 [+0.65, +1.34] | +0.03 [-0.01, +0.08] | -0.36 [-0.49, -0.25] | -11.8 [-16.1, -8.2] | 1.9e-06 / 1.7e-05 | 0.43 / 1 |
| DRIVE | U-Net | RGR-P | +3.47 [+3.00, +4.01] | -0.16 [-0.29, -0.03] | -1.69 [-1.90, -1.50] | -54.7 [-59.8, -49.7] | 1.9e-06 / 1.7e-05 | 0.048 / 0.31 |
| DRIVE | U-Net | RGR-P, setting re-selected per run | +3.47 [+3.00, +4.01] | -0.16 [-0.29, -0.03] | -1.69 [-1.90, -1.50] | -54.7 [-59.8, -49.7] | 1.9e-06 / 1.7e-05 | 0.048 / 0.31 |
| DRIVE | U-Net | RGR-P, recall-oriented | +4.79 [+4.22, +5.43] | -0.41 [-0.62, -0.21] | -2.67 [-2.99, -2.38] | -65.0 [-71.0, -58.9] | 1.9e-06 / 1.7e-05 | 0.001 / 0.0081 |
| DRIVE | U-Net | Hysteresis 0.25 | +7.94 [+7.45, +8.43] | -0.85 [-1.62, -0.13] | -7.58 [-7.98, -7.23] | -52.5 [-57.8, -47.5] | 1.9e-06 / 1.7e-05 | 0.076 / 0.3 |
| DRIVE | U-Net | Threshold selected | +3.54 [+3.29, +3.79] | +0.02 [-0.28, +0.31] | -2.75 [-2.91, -2.61] | -2.0 [-5.5, +1.4] | 1.9e-06 / 1.7e-05 | 0.7 / 1 |
| DRIVE | U-Net | Dense CRF | -0.90 [-0.96, -0.84] | -0.05 [-0.12, +0.02] | +0.52 [+0.46, +0.58] | -0.7 [-3.1, +1.8] | 1.9e-06 / 1.7e-05 | 0.07 / 0.28 |
| DRIVE | U-Net | DTI as released | +5.83 [+5.49, +6.17] | -0.39 [-0.98, +0.16] | -5.58 [-5.91, -5.30] | -46.8 [-51.6, -42.2] | 1.9e-06 / 1.7e-05 | 0.29 / 1 |
| DRIVE | Attention U-Net | RGR | +1.60 [+1.11, +2.20] | +0.01 [-0.05, +0.08] | -0.67 [-0.90, -0.48] | -12.8 [-16.7, -9.5] | 1.9e-06 / 1.7e-05 | 0.96 / 1 |
| DRIVE | Attention U-Net | Conservative-gate RGR | +0.92 [+0.62, +1.29] | +0.04 [-0.00, +0.09] | -0.32 [-0.45, -0.22] | -10.0 [-13.3, -7.2] | 1.9e-06 / 1.7e-05 | 0.19 / 1 |
| DRIVE | Attention U-Net | RGR-P | +3.36 [+2.89, +3.89] | -0.13 [-0.25, -0.01] | -1.58 [-1.77, -1.39] | -51.0 [-56.5, -45.4] | 1.9e-06 / 1.7e-05 | 0.07 / 0.35 |
| DRIVE | Attention U-Net | RGR-P, setting re-selected per run | +3.36 [+2.89, +3.89] | -0.13 [-0.25, -0.01] | -1.58 [-1.77, -1.39] | -51.0 [-56.5, -45.4] | 1.9e-06 / 1.7e-05 | 0.07 / 0.35 |
| DRIVE | Attention U-Net | RGR-P, recall-oriented | +4.61 [+4.04, +5.24] | -0.38 [-0.56, -0.21] | -2.51 [-2.81, -2.21] | -59.4 [-65.7, -52.9] | 1.9e-06 / 1.7e-05 | 0.00085 / 0.0077 |
| DRIVE | Attention U-Net | Hysteresis 0.25 | +8.21 [+7.67, +8.75] | -0.84 [-1.59, -0.12] | -7.64 [-8.05, -7.30] | -50.0 [-55.2, -44.9] | 1.9e-06 / 1.7e-05 | 0.058 / 0.29 |
| DRIVE | Attention U-Net | Threshold selected | +3.16 [+2.95, +3.38] | +0.07 [-0.20, +0.32] | -2.45 [-2.61, -2.31] | -2.4 [-6.6, +1.3] | 1.9e-06 / 1.7e-05 | 0.5 / 1 |
| DRIVE | Attention U-Net | Dense CRF | -0.94 [-1.03, -0.86] | -0.07 [-0.13, -0.00] | +0.51 [+0.47, +0.57] | -0.7 [-3.4, +2.3] | 1.9e-06 / 1.7e-05 | 0.021 / 0.15 |
| DRIVE | Attention U-Net | DTI as released | +5.92 [+5.56, +6.28] | -0.38 [-0.96, +0.17] | -5.60 [-5.92, -5.32] | -44.5 [-49.6, -39.5] | 1.9e-06 / 1.7e-05 | 0.35 / 1 |
| DRIVE | U-Net++ | RGR | +1.50 [+1.03, +2.09] | -0.00 [-0.08, +0.07] | -0.66 [-0.91, -0.46] | -10.3 [-14.2, -7.1] | 1.9e-06 / 1.7e-05 | 0.93 / 1 |
| DRIVE | U-Net++ | Conservative-gate RGR | +0.81 [+0.55, +1.15] | +0.02 [-0.01, +0.05] | -0.32 [-0.46, -0.21] | -7.9 [-11.0, -5.4] | 1.9e-06 / 1.7e-05 | 0.37 / 1 |
| DRIVE | U-Net++ | RGR-P | +2.86 [+2.41, +3.38] | -0.15 [-0.26, -0.04] | -1.42 [-1.61, -1.25] | -41.5 [-46.1, -36.8] | 1.9e-06 / 1.7e-05 | 0.033 / 0.29 |
| DRIVE | U-Net++ | RGR-P, setting re-selected per run | +3.11 [+2.63, +3.66] | -0.19 [-0.32, -0.07] | -1.58 [-1.81, -1.37] | -46.3 [-51.1, -41.3] | 1.9e-06 / 1.7e-05 | 0.024 / 0.22 |
| DRIVE | U-Net++ | RGR-P, recall-oriented | +4.05 [+3.50, +4.65] | -0.42 [-0.61, -0.26] | -2.37 [-2.66, -2.09] | -48.8 [-53.8, -43.8] | 1.9e-06 / 1.7e-05 | 3.6e-05 / 0.00036 |
| DRIVE | U-Net++ | Hysteresis 0.25 | +7.72 [+7.18, +8.25] | -0.96 [-1.70, -0.27] | -7.40 [-7.82, -7.05] | -40.8 [-45.5, -36.0] | 1.9e-06 / 1.7e-05 | 0.027 / 0.16 |
| DRIVE | U-Net++ | Threshold selected | +3.54 [+3.30, +3.78] | -0.07 [-0.39, +0.23] | -2.93 [-3.13, -2.76] | -3.3 [-7.4, +1.0] | 1.9e-06 / 1.7e-05 | 0.78 / 1 |
| DRIVE | U-Net++ | Dense CRF | -0.85 [-0.95, -0.75] | -0.05 [-0.12, +0.03] | +0.52 [+0.46, +0.59] | -0.7 [-3.1, +1.7] | 1.9e-06 / 1.7e-05 | 0.083 / 0.28 |
| DRIVE | U-Net++ | DTI as released | +5.54 [+5.18, +5.91] | -0.49 [-1.05, +0.05] | -5.41 [-5.75, -5.12] | -35.8 [-40.2, -31.3] | 1.9e-06 / 1.7e-05 | 0.2 / 1 |
| CHASE_DB1 | U-Net | RGR | +4.91 [+4.20, +5.70] | -0.65 [-0.88, -0.42] | -3.66 [-3.83, -3.47] | -22.4 [-27.1, -17.5] | 0.0078 / 0.023 | 0.0078 / 0.078 |
| CHASE_DB1 | U-Net | Conservative-gate RGR | +2.29 [+1.87, +2.78] | -0.15 [-0.26, -0.03] | -1.53 [-1.73, -1.39] | -13.4 [-17.1, -10.2] | 0.0078 / 0.023 | 0.078 / 0.7 |
| CHASE_DB1 | U-Net | RGR-P | +5.46 [+4.68, +6.29] | -0.70 [-0.94, -0.46] | -3.89 [-4.11, -3.71] | -38.6 [-45.8, -31.1] | 0.0078 / 0.023 | 0.0078 / 0.078 |
| CHASE_DB1 | U-Net | RGR-P, setting re-selected per run | +5.46 [+4.68, +6.29] | -0.70 [-0.94, -0.46] | -3.89 [-4.11, -3.71] | -38.6 [-45.8, -31.1] | 0.0078 / 0.023 | 0.0078 / 0.078 |
| CHASE_DB1 | U-Net | RGR-P, recall-oriented | +6.83 [+5.80, +7.92] | -0.84 [-1.13, -0.57] | -4.48 [-4.73, -4.26] | -56.5 [-66.4, -47.0] | 0.0078 / 0.023 | 0.0078 / 0.055 |
| CHASE_DB1 | U-Net | Hysteresis 0.25 | +7.32 [+6.18, +8.62] | -1.59 [-2.17, -1.06] | -7.08 [-7.40, -6.80] | -33.0 [-39.5, -26.0] | 0.0078 / 0.023 | 0.0078 / 0.07 |
| CHASE_DB1 | U-Net | Threshold selected | +3.16 [+2.62, +3.80] | -0.33 [-0.58, -0.08] | -2.61 [-2.74, -2.51] | +9.8 [+4.0, +16.4] | 0.0078 / 0.023 | 0.078 / 0.78 |
| CHASE_DB1 | U-Net | Dense CRF | -0.60 [-0.67, -0.53] | -0.06 [-0.06, -0.05] | -0.04 [-0.07, -0.00] | -2.2 [-6.0, +1.8] | 0.0078 / 0.023 | 0.0078 / 0.07 |
| CHASE_DB1 | U-Net | DTI as released | +5.20 [+4.41, +6.09] | -1.04 [-1.48, -0.63] | -5.27 [-5.52, -5.06] | -17.5 [-26.8, -8.2] | 0.0078 / 0.023 | 0.0078 / 0.078 |
| CHASE_DB1 | Attention U-Net | RGR | +4.87 [+4.19, +5.50] | -0.59 [-0.82, -0.33] | -3.77 [-3.96, -3.59] | -23.0 [-26.9, -19.1] | 0.0078 / 0.023 | 0.016 / 0.14 |
| CHASE_DB1 | Attention U-Net | Conservative-gate RGR | +2.17 [+1.76, +2.62] | -0.09 [-0.20, +0.05] | -1.54 [-1.73, -1.41] | -13.5 [-15.8, -11.5] | 0.0078 / 0.023 | 0.31 / 1 |
| CHASE_DB1 | Attention U-Net | RGR-P | +5.66 [+4.85, +6.42] | -0.58 [-0.84, -0.29] | -3.98 [-4.19, -3.76] | -39.5 [-47.2, -32.5] | 0.0078 / 0.023 | 0.039 / 0.31 |
| CHASE_DB1 | Attention U-Net | RGR-P, setting re-selected per run | +5.66 [+4.85, +6.42] | -0.58 [-0.84, -0.29] | -3.98 [-4.19, -3.76] | -39.5 [-47.2, -32.5] | 0.0078 / 0.023 | 0.039 / 0.31 |
| CHASE_DB1 | Attention U-Net | RGR-P, recall-oriented | +7.13 [+5.96, +8.32] | -0.71 [-1.06, -0.31] | -4.58 [-4.94, -4.29] | -59.2 [-70.4, -48.4] | 0.0078 / 0.023 | 0.039 / 0.23 |
| CHASE_DB1 | Attention U-Net | Hysteresis 0.25 | +7.46 [+6.46, +8.62] | -1.31 [-1.80, -0.74] | -6.99 [-7.27, -6.73] | -34.6 [-41.1, -28.2] | 0.0078 / 0.023 | 0.016 / 0.12 |
| CHASE_DB1 | Attention U-Net | Threshold selected | +2.82 [+2.57, +3.15] | -0.11 [-0.30, +0.13] | -2.23 [-2.32, -2.14] | +11.1 [+7.0, +15.0] | 0.0078 / 0.023 | 0.38 / 1 |
| CHASE_DB1 | Attention U-Net | Dense CRF | -0.64 [-0.81, -0.47] | -0.07 [-0.09, -0.05] | -0.06 [-0.09, -0.04] | -4.9 [-8.2, -2.2] | 0.0078 / 0.023 | 0.0078 / 0.07 |
| CHASE_DB1 | Attention U-Net | DTI as released | +5.29 [+4.60, +6.06] | -0.76 [-1.14, -0.32] | -5.15 [-5.35, -4.97] | -25.4 [-32.2, -18.8] | 0.0078 / 0.023 | 0.039 / 0.31 |
| CHASE_DB1 | U-Net++ | RGR | +4.68 [+4.26, +5.11] | -0.56 [-0.81, -0.28] | -3.75 [-3.90, -3.60] | -18.4 [-20.1, -16.9] | 0.0078 / 0.023 | 0.023 / 0.19 |
| CHASE_DB1 | U-Net++ | Conservative-gate RGR | +2.16 [+1.81, +2.56] | -0.07 [-0.19, +0.06] | -1.54 [-1.73, -1.40] | -11.6 [-13.5, -9.8] | 0.0078 / 0.023 | 0.46 / 1 |
| CHASE_DB1 | U-Net++ | RGR-P | +5.38 [+4.70, +6.12] | -0.56 [-0.83, -0.25] | -3.96 [-4.09, -3.86] | -35.8 [-43.1, -28.7] | 0.0078 / 0.023 | 0.039 / 0.31 |
| CHASE_DB1 | U-Net++ | RGR-P, setting re-selected per run | +5.93 [+5.15, +6.80] | -0.58 [-0.88, -0.24] | -4.14 [-4.25, -4.03] | -46.9 [-56.5, -37.4] | 0.0078 / 0.023 | 0.039 / 0.31 |
| CHASE_DB1 | U-Net++ | RGR-P, recall-oriented | +6.66 [+5.80, +7.73] | -0.67 [-0.99, -0.28] | -4.49 [-4.69, -4.31] | -51.8 [-60.8, -42.6] | 0.0078 / 0.023 | 0.039 / 0.23 |
| CHASE_DB1 | U-Net++ | Hysteresis 0.25 | +7.24 [+6.27, +8.54] | -1.21 [-1.76, -0.59] | -6.85 [-7.10, -6.67] | -30.2 [-36.4, -24.4] | 0.0078 / 0.023 | 0.023 / 0.16 |
| CHASE_DB1 | U-Net++ | Threshold selected | +3.43 [+2.98, +3.99] | -0.18 [-0.43, +0.11] | -2.75 [-2.85, -2.67] | +7.0 [+1.1, +12.9] | 0.0078 / 0.023 | 0.38 / 1 |
| CHASE_DB1 | U-Net++ | Dense CRF | -0.65 [-0.79, -0.51] | -0.05 [-0.07, -0.02] | -0.03 [-0.08, +0.01] | -2.2 [-4.6, +0.1] | 0.0078 / 0.023 | 0.039 / 0.2 |
| CHASE_DB1 | U-Net++ | DTI as released | +5.14 [+4.40, +6.03] | -0.71 [-1.13, -0.25] | -5.06 [-5.26, -4.91] | -21.2 [-28.4, -13.5] | 0.0078 / 0.023 | 0.039 / 0.31 |
| STARE | U-Net | RGR | +3.47 [+2.66, +4.16] | +0.19 [-0.08, +0.47] | -1.29 [-1.70, -0.89] | -22.6 [-31.4, -14.6] | 0.002 / 0.012 | 0.32 / 1 |
| STARE | U-Net | Conservative-gate RGR | +1.43 [+0.92, +1.88] | +0.15 [+0.04, +0.28] | -0.40 [-0.58, -0.28] | -12.7 [-18.5, -7.4] | 0.002 / 0.012 | 0.037 / 0.37 |
| STARE | U-Net | RGR-P | +4.35 [+3.67, +5.00] | +0.20 [-0.15, +0.55] | -1.76 [-2.21, -1.38] | -44.9 [-57.9, -34.6] | 0.002 / 0.012 | 0.49 / 1 |
| STARE | U-Net | RGR-P, setting re-selected per run | +4.35 [+3.67, +5.00] | +0.20 [-0.15, +0.55] | -1.76 [-2.21, -1.38] | -44.9 [-57.9, -34.6] | 0.002 / 0.012 | 0.49 / 1 |
| STARE | U-Net | RGR-P, recall-oriented | +5.41 [+4.67, +6.17] | +0.01 [-0.46, +0.46] | -2.58 [-3.19, -2.06] | -58.7 [-75.4, -45.4] | 0.002 / 0.012 | 1 / 1 |
| STARE | U-Net | Hysteresis 0.25 | +6.26 [+5.48, +7.15] | +0.10 [-0.83, +1.17] | -6.41 [-7.03, -5.83] | -42.5 [-53.8, -33.2] | 0.002 / 0.012 | 1 / 1 |
| STARE | U-Net | Threshold selected | +2.78 [+2.39, +3.17] | +0.36 [-0.00, +0.74] | -2.25 [-2.47, -2.05] | -3.5 [-8.9, +1.3] | 0.002 / 0.012 | 0.084 / 0.78 |
| STARE | U-Net | Dense CRF | -0.76 [-0.88, -0.64] | -0.07 [-0.13, -0.01] | +0.23 [+0.19, +0.28] | -3.5 [-7.3, +0.3] | 0.002 / 0.012 | 0.027 / 0.16 |
| STARE | U-Net | DTI as released | +4.47 [+3.90, +5.10] | +0.27 [-0.42, +1.05] | -4.69 [-5.12, -4.28] | -35.4 [-45.4, -26.9] | 0.002 / 0.012 | 0.62 / 1 |
| STARE | Attention U-Net | RGR | +3.29 [+2.46, +3.90] | +0.05 [-0.24, +0.33] | -1.48 [-1.90, -1.07] | -23.7 [-35.5, -13.7] | 0.002 / 0.012 | 1 / 1 |
| STARE | Attention U-Net | Conservative-gate RGR | +1.28 [+0.77, +1.70] | +0.09 [-0.03, +0.21] | -0.48 [-0.67, -0.34] | -14.7 [-23.5, -7.8] | 0.002 / 0.012 | 0.43 / 1 |
| STARE | Attention U-Net | RGR-P | +4.22 [+3.34, +4.99] | -0.02 [-0.36, +0.30] | -2.01 [-2.51, -1.60] | -45.8 [-63.9, -33.4] | 0.002 / 0.012 | 0.77 / 1 |
| STARE | Attention U-Net | RGR-P, setting re-selected per run | +4.22 [+3.34, +4.99] | -0.02 [-0.36, +0.30] | -2.01 [-2.51, -1.60] | -45.8 [-63.9, -33.4] | 0.002 / 0.012 | 0.77 / 1 |
| STARE | Attention U-Net | RGR-P, recall-oriented | +5.30 [+4.33, +6.32] | -0.19 [-0.61, +0.23] | -2.77 [-3.41, -2.27] | -57.8 [-79.8, -43.2] | 0.002 / 0.012 | 0.38 / 1 |
| STARE | Attention U-Net | Hysteresis 0.25 | +6.07 [+5.26, +6.85] | -0.24 [-1.14, +0.67] | -6.55 [-7.07, -6.12] | -42.2 [-57.2, -31.8] | 0.002 / 0.012 | 0.49 / 1 |
| STARE | Attention U-Net | Threshold selected | +2.40 [+2.08, +2.70] | +0.22 [-0.10, +0.53] | -2.10 [-2.29, -1.93] | -1.6 [-8.1, +4.3] | 0.002 / 0.012 | 0.28 / 1 |
| STARE | Attention U-Net | Dense CRF | -0.76 [-0.90, -0.63] | -0.06 [-0.11, +0.00] | +0.22 [+0.17, +0.28] | -0.9 [-3.6, +1.9] | 0.002 / 0.012 | 0.084 / 0.28 |
| STARE | Attention U-Net | DTI as released | +4.41 [+3.82, +4.99] | +0.02 [-0.67, +0.71] | -4.82 [-5.23, -4.49] | -37.7 [-52.0, -27.6] | 0.002 / 0.012 | 0.85 / 1 |
| STARE | U-Net++ | RGR | +3.16 [+2.45, +3.76] | +0.14 [-0.16, +0.42] | -1.38 [-1.85, -0.94] | -17.9 [-25.4, -11.2] | 0.002 / 0.012 | 0.49 / 1 |
| STARE | U-Net++ | Conservative-gate RGR | +1.20 [+0.84, +1.53] | +0.13 [+0.01, +0.25] | -0.42 [-0.62, -0.29] | -11.0 [-16.4, -6.6] | 0.002 / 0.012 | 0.11 / 0.84 |
| STARE | U-Net++ | RGR-P | +3.68 [+3.01, +4.26] | +0.12 [-0.21, +0.43] | -1.66 [-2.14, -1.24] | -31.5 [-41.4, -23.5] | 0.002 / 0.012 | 0.56 / 1 |
| STARE | U-Net++ | RGR-P, setting re-selected per run | +3.96 [+3.24, +4.60] | +0.12 [-0.22, +0.43] | -1.78 [-2.30, -1.34] | -37.7 [-50.8, -27.9] | 0.002 / 0.012 | 0.56 / 1 |
| STARE | U-Net++ | RGR-P, recall-oriented | +4.51 [+3.71, +5.30] | -0.04 [-0.49, +0.36] | -2.36 [-2.98, -1.86] | -42.5 [-55.9, -31.9] | 0.002 / 0.012 | 0.85 / 1 |
| STARE | U-Net++ | Hysteresis 0.25 | +6.08 [+5.31, +6.96] | +0.13 [-0.79, +1.07] | -6.14 [-6.77, -5.60] | -29.4 [-37.0, -23.0] | 0.002 / 0.012 | 0.85 / 1 |
| STARE | U-Net++ | Threshold selected | +2.86 [+2.53, +3.25] | +0.39 [-0.01, +0.79] | -2.35 [-2.62, -2.12] | +3.0 [-3.1, +9.5] | 0.002 / 0.012 | 0.13 / 0.92 |
| STARE | U-Net++ | Dense CRF | -0.62 [-0.68, -0.55] | -0.03 [-0.08, +0.02] | +0.25 [+0.19, +0.31] | -1.8 [-4.6, +1.0] | 0.002 / 0.012 | 0.49 / 0.49 |
| STARE | U-Net++ | DTI as released | +4.19 [+3.63, +4.84] | +0.31 [-0.38, +1.02] | -4.44 [-4.91, -4.03] | -25.2 [-32.4, -18.9] | 0.002 / 0.012 | 0.62 / 1 |
| FIVES | U-Net | RGR | +4.32 [+3.82, +4.95] | -0.93 [-1.53, -0.40] | -4.09 [-5.08, -3.21] | -62.5 [-74.8, -52.4] | 1.8e-12 / 2.2e-11 | 0.00071 / 0.0079 |
| FIVES | U-Net | Conservative-gate RGR | +2.68 [+2.19, +3.30] | -0.78 [-1.60, -0.16] | -3.15 [-4.72, -1.91] | -50.6 [-63.4, -40.2] | 1.8e-12 / 2.2e-11 | 0.031 / 0.34 |
| FIVES | U-Net | RGR-P | +5.01 [+4.50, +5.64] | -1.07 [-1.72, -0.51] | -4.55 [-5.60, -3.63] | -203.7 [-252.0, -163.3] | 1.8e-12 / 2.2e-11 | 0.00014 / 0.0015 |
| FIVES | U-Net | RGR-P, setting re-selected per run | +5.01 [+4.50, +5.64] | -1.07 [-1.72, -0.51] | -4.55 [-5.60, -3.63] | -203.7 [-252.0, -163.3] | 1.8e-12 / 2.2e-11 | 0.00014 / 0.0015 |
| FIVES | U-Net | RGR-P, recall-oriented | +6.62 [+6.01, +7.35] | -1.40 [-2.14, -0.75] | -5.52 [-6.67, -4.49] | -254.1 [-305.3, -211.5] | 1.8e-12 / 2.2e-11 | 3.1e-05 / 0.00034 |
| FIVES | U-Net | Hysteresis 0.25 | +6.87 [+6.15, +7.74] | -3.58 [-4.49, -2.64] | -10.83 [-11.73, -9.94] | -197.6 [-255.0, -151.5] | 1.8e-12 / 2.2e-11 | 2e-06 / 2.2e-05 |
| FIVES | U-Net | Threshold selected | +2.93 [+2.63, +3.31] | -0.97 [-1.34, -0.60] | -4.01 [-4.44, -3.61] | +68.2 [+35.4, +97.3] | 1.8e-12 / 2.2e-11 | 5.8e-05 / 0.00064 |
| FIVES | U-Net | DTI as released | +4.34 [+3.88, +4.88] | -2.22 [-2.83, -1.57] | -7.57 [-8.16, -6.98] | +35.2 [-30.9, +91.8] | 1.8e-12 / 2.2e-11 | 4.5e-06 / 5e-05 |
| FIVES | Attention U-Net | RGR | +3.41 [+3.06, +3.84] | -0.89 [-1.41, -0.48] | -3.55 [-4.48, -2.77] | -44.1 [-52.4, -36.8] | 1.8e-12 / 2.2e-11 | 3.2e-06 / 3.8e-05 |
| FIVES | Attention U-Net | Conservative-gate RGR | +1.92 [+1.55, +2.39] | -0.66 [-1.43, -0.18] | -2.48 [-3.97, -1.43] | -33.2 [-41.0, -26.5] | 1.8e-12 / 2.2e-11 | 0.0023 / 0.027 |
| FIVES | Attention U-Net | RGR-P | +3.90 [+3.53, +4.35] | -1.05 [-1.60, -0.62] | -3.99 [-4.98, -3.17] | -178.7 [-217.5, -143.4] | 1.8e-12 / 2.2e-11 | 1.2e-06 / 1.4e-05 |
| FIVES | Attention U-Net | RGR-P, setting re-selected per run | +3.90 [+3.53, +4.35] | -1.05 [-1.60, -0.62] | -3.99 [-4.98, -3.17] | -178.7 [-217.5, -143.4] | 1.8e-12 / 2.2e-11 | 1.2e-06 / 1.4e-05 |
| FIVES | Attention U-Net | RGR-P, recall-oriented | +5.11 [+4.61, +5.70] | -1.37 [-2.01, -0.86] | -4.87 [-5.98, -3.93] | -216.9 [-258.4, -179.2] | 1.8e-12 / 2.2e-11 | 7.1e-07 / 8.6e-06 |
| FIVES | Attention U-Net | Hysteresis 0.25 | +5.47 [+4.89, +6.18] | -3.42 [-4.18, -2.68] | -9.83 [-10.76, -9.01] | -184.5 [-229.8, -143.9] | 1.8e-12 / 2.2e-11 | 7.1e-07 / 8.6e-06 |
| FIVES | Attention U-Net | Threshold selected | +2.08 [+1.86, +2.35] | -0.83 [-1.08, -0.59] | -3.19 [-3.53, -2.90] | +50.5 [+31.5, +68.6] | 1.8e-12 / 2.2e-11 | 3.5e-06 / 4.2e-05 |
| FIVES | Attention U-Net | DTI as released | +3.50 [+3.12, +3.98] | -2.16 [-2.64, -1.66] | -6.89 [-7.45, -6.38] | +35.4 [-10.4, +78.9] | 1.8e-12 / 2.2e-11 | 1.3e-06 / 1.5e-05 |
| FIVES | U-Net++ | RGR | +4.55 [+4.04, +5.16] | -0.31 [-0.78, +0.14] | -3.45 [-4.33, -2.69] | -42.0 [-49.7, -35.0] | 1.8e-12 / 2.2e-11 | 0.59 / 1 |
| FIVES | U-Net++ | Conservative-gate RGR | +2.65 [+2.16, +3.26] | -0.27 [-0.80, +0.16] | -2.42 [-3.64, -1.46] | -32.1 [-39.9, -25.2] | 1.8e-12 / 2.2e-11 | 0.25 / 1 |
| FIVES | U-Net++ | RGR-P | +5.11 [+4.59, +5.75] | -0.39 [-0.88, +0.07] | -3.79 [-4.72, -2.99] | -149.7 [-194.9, -113.2] | 1.8e-12 / 2.2e-11 | 0.47 / 1 |
| FIVES | U-Net++ | RGR-P, setting re-selected per run | +5.71 [+5.14, +6.40] | -0.42 [-0.94, +0.07] | -4.00 [-4.96, -3.17] | -173.7 [-221.4, -135.0] | 1.8e-12 / 2.2e-11 | 0.45 / 1 |
| FIVES | U-Net++ | RGR-P, recall-oriented | +6.63 [+6.00, +7.39] | -0.60 [-1.17, -0.07] | -4.62 [-5.66, -3.72] | -190.0 [-238.2, -150.8] | 1.8e-12 / 2.2e-11 | 0.21 / 0.83 |
| FIVES | U-Net++ | Hysteresis 0.25 | +6.94 [+6.21, +7.83] | -2.14 [-2.97, -1.25] | -9.32 [-10.24, -8.43] | -144.5 [-190.0, -107.1] | 1.8e-12 / 2.2e-11 | 0.0012 / 0.012 |
| FIVES | U-Net++ | Threshold selected | +3.31 [+2.96, +3.74] | -0.53 [-0.89, -0.14] | -3.78 [-4.23, -3.36] | +65.4 [+46.0, +84.1] | 1.8e-12 / 2.2e-11 | 0.11 / 0.87 |
| FIVES | U-Net++ | DTI as released | +4.20 [+3.77, +4.73] | -1.26 [-1.83, -0.64] | -6.48 [-7.08, -5.90] | +53.2 [+10.9, +92.4] | 1.8e-12 / 2.2e-11 | 0.009 / 0.081 |


**T_calib.** Conservative-gate RGR with the estimates of Eq. S5 computed from bin-wise recalibrated probabilities; the gates stay on the network probability.

| Dataset | Network | Recalibration (fitted on 4 DRIVE validation images) | ECE on test | Dice | TCR | Frag |
|---|---|---|---|---|---|---|
| DRIVE | U-Net | none (published rule) | 0.0119 | 0.8257 | 0.6994 | 63.5 |
| DRIVE | U-Net | histogram binning (15 bins) | 0.0129 | 0.8256 | 0.7034 | 61.9 |
| DRIVE | U-Net | isotonic regression | 0.0115 | 0.8256 | 0.7037 | 61.8 |
| DRIVE | Attention U-Net | none (published rule) | 0.0119 | 0.8266 | 0.6998 | 58.2 |
| DRIVE | Attention U-Net | histogram binning (15 bins) | 0.0134 | 0.8266 | 0.7044 | 56.0 |
| DRIVE | Attention U-Net | isotonic regression | 0.0124 | 0.8266 | 0.7044 | 56.2 |
| DRIVE | U-Net++ | none (published rule) | 0.0125 | 0.8276 | 0.7043 | 47.9 |
| DRIVE | U-Net++ | histogram binning (15 bins) | 0.0135 | 0.8277 | 0.7078 | 46.7 |
| DRIVE | U-Net++ | isotonic regression | 0.0121 | 0.8276 | 0.7075 | 46.6 |
| CHASE_DB1 | U-Net | none (published rule) | 0.0135 | 0.8071 | 0.7126 | 57.9 |
| CHASE_DB1 | U-Net | histogram binning (15 bins) | 0.0222 | 0.8046 | 0.7273 | 52.1 |
| CHASE_DB1 | U-Net | isotonic regression | 0.0162 | 0.8053 | 0.7234 | 54.0 |
| CHASE_DB1 | Attention U-Net | none (published rule) | 0.0130 | 0.8092 | 0.6960 | 60.8 |
| CHASE_DB1 | Attention U-Net | histogram binning (15 bins) | 0.0204 | 0.8067 | 0.7129 | 54.1 |
| CHASE_DB1 | Attention U-Net | isotonic regression | 0.0140 | 0.8076 | 0.7086 | 56.0 |
| CHASE_DB1 | U-Net++ | none (published rule) | 0.0126 | 0.8093 | 0.7135 | 55.8 |
| CHASE_DB1 | U-Net++ | histogram binning (15 bins) | 0.0193 | 0.8071 | 0.7283 | 51.5 |
| CHASE_DB1 | U-Net++ | isotonic regression | 0.0124 | 0.8086 | 0.7201 | 53.6 |
| STARE | U-Net | none (published rule) | 0.0091 | 0.8439 | 0.7915 | 56.9 |
| STARE | U-Net | histogram binning (15 bins) | 0.0170 | 0.8443 | 0.8043 | 50.2 |
| STARE | U-Net | isotonic regression | 0.0079 | 0.8440 | 0.7933 | 56.0 |
| STARE | Attention U-Net | none (published rule) | 0.0086 | 0.8483 | 0.8028 | 51.9 |
| STARE | Attention U-Net | histogram binning (15 bins) | 0.0174 | 0.8481 | 0.8134 | 46.1 |
| STARE | Attention U-Net | isotonic regression | 0.0075 | 0.8483 | 0.8057 | 49.5 |
| STARE | U-Net++ | none (published rule) | 0.0091 | 0.8512 | 0.8053 | 40.0 |
| STARE | U-Net++ | histogram binning (15 bins) | 0.0182 | 0.8514 | 0.8114 | 36.4 |
| STARE | U-Net++ | isotonic regression | 0.0076 | 0.8508 | 0.8007 | 44.1 |
| FIVES | U-Net | none (published rule) | 0.0165 | 0.8255 | 0.7769 | 339.8 |
| FIVES | U-Net | histogram binning (15 bins) | 0.0269 | 0.8211 | 0.7880 | 330.4 |
| FIVES | U-Net | isotonic regression | 0.0414 | 0.8193 | 0.7959 | 326.1 |
| FIVES | Attention U-Net | none (published rule) | 0.0156 | 0.8373 | 0.7902 | 306.1 |
| FIVES | Attention U-Net | histogram binning (15 bins) | 0.0270 | 0.8340 | 0.7990 | 299.6 |
| FIVES | Attention U-Net | isotonic regression | 0.0417 | 0.8310 | 0.8062 | 295.2 |
| FIVES | U-Net++ | none (published rule) | 0.0074 | 0.8316 | 0.7354 | 269.3 |
| FIVES | U-Net++ | histogram binning (15 bins) | 0.0203 | 0.8290 | 0.7466 | 262.9 |
| FIVES | U-Net++ | isotonic regression | 0.0343 | 0.8284 | 0.7550 | 258.9 |


**T_obs2.** Second observer: thin-centreline recall of observer 2 against observer 1 (the human ceiling) and the additions of RGR re-scored against observer 2.

| Dataset | Network | Variant | Observer-2 TCR vs observer 1 (%) | Dice obs2 vs obs1 | Added pixels | False by observer 1 | Of these: vessel by observer 2 (%) | Within 1.5 px of observer-2 vessel (%) | Added pixels on observer-2 vessel (%) |
|---|---|---|---|---|---|---|---|---|---|
| CHASE_DB1 | U-Net | RGR | 78.2 | 0.7973 | 45745 | 30654 | 28.4 | 74.5 | 40.5 |
| CHASE_DB1 | U-Net | Conservative-gate RGR | 78.2 | 0.7973 | 19936 | 12618 | 30.9 | 77.4 | 44.1 |
| CHASE_DB1 | U-Net | RGR-P | 78.2 | 0.7973 | 48928 | 32807 | 28.1 | 72.5 | 40.4 |
| CHASE_DB1 | U-Net | RGR-P, setting re-selected per run | 78.2 | 0.7973 | 48928 | 32807 | 28.1 | 72.5 | 40.4 |
| CHASE_DB1 | U-Net | RGR-P, recall-oriented | 78.2 | 0.7973 | 56508 | 38131 | 27.1 | 67.7 | 39.4 |
| CHASE_DB1 | Attention U-Net | RGR | 78.2 | 0.7973 | 46150 | 30525 | 29.6 | 76.0 | 41.4 |
| CHASE_DB1 | Attention U-Net | Conservative-gate RGR | 78.2 | 0.7973 | 19908 | 12280 | 32.7 | 78.9 | 45.8 |
| CHASE_DB1 | Attention U-Net | RGR-P | 78.2 | 0.7973 | 49568 | 32496 | 29.9 | 74.9 | 41.8 |
| CHASE_DB1 | Attention U-Net | RGR-P, setting re-selected per run | 78.2 | 0.7973 | 49568 | 32496 | 29.9 | 74.9 | 41.8 |
| CHASE_DB1 | Attention U-Net | RGR-P, recall-oriented | 78.2 | 0.7973 | 57358 | 37839 | 28.8 | 70.2 | 41.2 |
| CHASE_DB1 | U-Net++ | RGR | 78.2 | 0.7973 | 46488 | 30548 | 29.8 | 75.2 | 41.8 |
| CHASE_DB1 | U-Net++ | Conservative-gate RGR | 78.2 | 0.7973 | 20220 | 12395 | 32.4 | 78.0 | 45.9 |
| CHASE_DB1 | U-Net++ | RGR-P | 78.2 | 0.7973 | 49861 | 32592 | 30.1 | 73.9 | 42.4 |
| CHASE_DB1 | U-Net++ | RGR-P, setting re-selected per run | 78.2 | 0.7973 | 52381 | 34208 | 29.8 | 72.7 | 42.1 |
| CHASE_DB1 | U-Net++ | RGR-P, recall-oriented | 78.2 | 0.7973 | 56682 | 37241 | 28.9 | 69.7 | 41.4 |
| STARE | U-Net | RGR | 93.6 | 0.7608 | 10261 | 5329 | 81.4 | 97.0 | 86.7 |
| STARE | U-Net | Conservative-gate RGR | 93.6 | 0.7608 | 3806 | 1716 | 83.9 | 96.9 | 89.6 |
| STARE | U-Net | RGR-P | 93.6 | 0.7608 | 13670 | 7287 | 73.2 | 93.9 | 81.3 |
| STARE | U-Net | RGR-P, setting re-selected per run | 93.6 | 0.7608 | 13670 | 7287 | 73.2 | 93.9 | 81.3 |
| STARE | U-Net | RGR-P, recall-oriented | 93.6 | 0.7608 | 18315 | 10577 | 65.7 | 88.7 | 75.7 |
| STARE | Attention U-Net | RGR | 93.6 | 0.7608 | 10886 | 6100 | 76.3 | 91.9 | 83.1 |
| STARE | Attention U-Net | Conservative-gate RGR | 93.6 | 0.7608 | 3968 | 2000 | 77.6 | 89.6 | 85.3 |
| STARE | Attention U-Net | RGR-P | 93.6 | 0.7608 | 14293 | 8315 | 70.1 | 90.7 | 78.1 |
| STARE | Attention U-Net | RGR-P, setting re-selected per run | 93.6 | 0.7608 | 14293 | 8315 | 70.1 | 90.7 | 78.1 |
| STARE | Attention U-Net | RGR-P, recall-oriented | 93.6 | 0.7608 | 18823 | 11452 | 63.2 | 87.2 | 72.9 |
| STARE | U-Net++ | RGR | 93.6 | 0.7608 | 10544 | 5615 | 83.3 | 97.6 | 87.1 |
| STARE | U-Net++ | Conservative-gate RGR | 93.6 | 0.7608 | 3748 | 1743 | 85.3 | 96.8 | 89.4 |
| STARE | U-Net++ | RGR-P | 93.6 | 0.7608 | 12389 | 6740 | 79.1 | 96.4 | 84.2 |
| STARE | U-Net++ | RGR-P, setting re-selected per run | 93.6 | 0.7608 | 13248 | 7248 | 78.2 | 95.8 | 83.5 |
| STARE | U-Net++ | RGR-P, recall-oriented | 93.6 | 0.7608 | 16379 | 9560 | 69.6 | 90.9 | 77.7 |


**T_missed.** Network probability of reference thin-vessel pixels removed by the 0.5 threshold, within the distance limit of the seed.

| Dataset | Network | Missed thin-vessel pixels within 8k px of the seed | p in [0.25, 0.5) (%) | p in [0.35, 0.5) (%) | p < 0.25 (%) |
|---|---|---|---|---|---|
| DRIVE | U-Net | 60207 | 41.8 | 25.6 | 58.2 |
| DRIVE | Attention U-Net | 59322 | 42.6 | 26.3 | 57.4 |
| DRIVE | U-Net++ | 57836 | 41.3 | 24.9 | 58.7 |
| CHASE_DB1 | U-Net | 46737 | 38.5 | 23.2 | 61.5 |
| CHASE_DB1 | Attention U-Net | 49627 | 37.7 | 23.0 | 62.3 |
| CHASE_DB1 | U-Net++ | 49245 | 37.9 | 22.9 | 62.1 |
| STARE | U-Net | 30156 | 43.8 | 26.4 | 56.2 |
| STARE | Attention U-Net | 30004 | 43.7 | 26.7 | 56.3 |
| STARE | U-Net++ | 29600 | 43.6 | 26.4 | 56.4 |
| FIVES | U-Net | 1030894 | 43.3 | 26.5 | 56.7 |
| FIVES | Attention U-Net | 911422 | 40.3 | 24.6 | 59.7 |
| FIVES | U-Net++ | 1128213 | 39.9 | 24.3 | 60.1 |


**T_seeds.** Mean +- SD over training seeds of the changes relative to the 0.5 threshold (percentage points).

| Dataset | Network | Seeds | RGR dTCR | RGR dDice | Conservative gate dTCR | Conservative gate dDice | RGR-P dTCR | RGR-P dDice | RGR-P dFrag | Margin TCR at equal precision | Margin clDice at equal precision |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DRIVE | U-Net | 3 | +1.59 +- 0.02 | -0.00 +- 0.01 | +0.94 +- 0.03 | +0.03 +- 0.01 | +3.53 +- 0.07 | -0.22 +- 0.05 | -59.10 +- 3.19 | +0.63 +- 0.02 | +0.03 +- 0.01 |
| DRIVE | Attention U-Net | 3 | +1.59 +- 0.04 | +0.01 +- 0.01 | +0.92 +- 0.03 | +0.04 +- 0.00 | +3.29 +- 0.08 | -0.15 +- 0.04 | -51.25 +- 1.22 | +0.67 +- 0.02 | +0.06 +- 0.01 |
| DRIVE | U-Net++ | 3 | +1.47 +- 0.07 | -0.02 +- 0.03 | +0.79 +- 0.05 | +0.02 +- 0.01 | +2.79 +- 0.12 | -0.16 +- 0.04 | -40.58 +- 1.10 | +0.60 +- 0.08 | -0.00 +- 0.04 |
| CHASE_DB1 | U-Net | 3 | +4.95 +- 0.20 | -0.58 +- 0.05 | +2.28 +- 0.08 | -0.10 +- 0.03 | +5.59 +- 0.19 | -0.59 +- 0.08 | -40.58 +- 3.04 | +0.45 +- 0.13 | -0.11 +- 0.06 |
| CHASE_DB1 | Attention U-Net | 3 | +4.93 +- 0.06 | -0.57 +- 0.03 | +2.28 +- 0.10 | -0.07 +- 0.01 | +5.63 +- 0.07 | -0.57 +- 0.02 | -42.21 +- 2.36 | +0.36 +- 0.07 | -0.09 +- 0.04 |
| CHASE_DB1 | U-Net++ | 3 | +4.75 +- 0.11 | -0.64 +- 0.09 | +2.22 +- 0.05 | -0.13 +- 0.05 | +5.40 +- 0.07 | -0.65 +- 0.10 | -36.12 +- 1.50 | +0.36 +- 0.23 | -0.19 +- 0.08 |
| STARE | U-Net | 3 | +3.57 +- 0.07 | +0.25 +- 0.05 | +1.51 +- 0.09 | +0.18 +- 0.02 | +4.38 +- 0.04 | +0.27 +- 0.07 | -42.50 +- 1.82 | +1.77 +- 0.07 | +0.39 +- 0.05 |
| STARE | Attention U-Net | 3 | +3.42 +- 0.12 | +0.20 +- 0.11 | +1.40 +- 0.08 | +0.15 +- 0.05 | +4.34 +- 0.10 | +0.19 +- 0.16 | -43.90 +- 1.59 | +1.60 +- 0.03 | +0.29 +- 0.03 |
| STARE | U-Net++ | 3 | +3.28 +- 0.08 | +0.21 +- 0.05 | +1.27 +- 0.05 | +0.16 +- 0.03 | +3.90 +- 0.17 | +0.19 +- 0.07 | -32.70 +- 1.56 | +1.55 +- 0.07 | +0.30 +- 0.07 |
