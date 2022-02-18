function back() {
        document.addEventListener('keydown', function (event) {
            if (event.ctrlKey && event.key === 'z') {
                window.history.back();
            }
        });
    }

    function forward() {
        document.addEventListener('keydown', function (event) {
            if (event.ctrlKey && event.key === 'y') {
                window.history.forward();
            }
        });
    }
