document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const splashScreen = document.getElementById('splashScreen');
    const enterPortfolioButton = document.getElementById('enterPortfolio');
    const navToggle = document.getElementById('navToggle');
    const navPanel = document.getElementById('navPanel');
    const chatToggle = document.getElementById('chatToggle');
    const chatContainer = document.getElementById('chatContainer');
    const chatClose = document.getElementById('chatClose');
    const chatMessages = document.getElementById('chatMessages');
    const chatMessageStack = document.getElementById('chatMessageStack');
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const splashTypedText = document.getElementById('splashTypedText');
    const heroTypedText = document.getElementById('heroTypedText');

    const appData = {
        resumeUrl: body.dataset.resumeUrl,
        certificateUrl: body.dataset.certificateUrl,
        email: body.dataset.email,
        phone: body.dataset.phone,
        phoneLink: body.dataset.phoneLink,
        linkedin: body.dataset.linkedin,
    };

    const pointer = { x: 0, y: 0 };
    let hasEntered = false;

    const getChatMessageHost = () => chatMessageStack || chatMessages;

    const scrollChatToLatest = (behavior = 'smooth') => {
        if (!chatMessages) {
            return;
        }

        window.requestAnimationFrame(() => {
            chatMessages.scrollTo({
                top: chatMessages.scrollHeight,
                behavior: prefersReducedMotion ? 'auto' : behavior,
            });
        });
    };

    const setNavOpen = (open) => {
        if (!navPanel || !navToggle) {
            return;
        }

        navPanel.classList.toggle('is-open', open);
        navToggle.setAttribute('aria-expanded', String(open));
    };

    const setChatOpen = (open) => {
        if (!chatContainer || !chatToggle) {
            return;
        }

        chatContainer.classList.toggle('is-open', open);
        chatContainer.setAttribute('aria-hidden', String(!open));
        chatToggle.setAttribute('aria-expanded', String(open));

        if (open) {
            window.setTimeout(() => {
                userInput?.focus();
                scrollChatToLatest('auto');
            }, 120);
        }
    };

    const smoothScrollToSection = (sectionId) => {
        const target = document.getElementById(sectionId);
        if (!target) {
            return;
        }

        const offsetTop = target.getBoundingClientRect().top + window.scrollY - 110;
        window.scrollTo({ top: offsetTop, behavior: prefersReducedMotion ? 'auto' : 'smooth' });
    };

    const startTypingEffect = (element, phrases, options = {}) => {
        if (!element || !phrases.length) {
            return;
        }

        if (prefersReducedMotion) {
            element.textContent = phrases[0];
            return;
        }

        const typingSpeed = options.typingSpeed ?? 48;
        const deletingSpeed = options.deletingSpeed ?? 24;
        const holdDelay = options.holdDelay ?? 1200;
        let phraseIndex = 0;
        let charIndex = 0;
        let deleting = false;

        const tick = () => {
            const phrase = phrases[phraseIndex];
            element.textContent = phrase.slice(0, charIndex);

            if (!deleting && charIndex < phrase.length) {
                charIndex += 1;
                window.setTimeout(tick, typingSpeed);
                return;
            }

            if (!deleting && charIndex === phrase.length) {
                deleting = true;
                window.setTimeout(tick, holdDelay);
                return;
            }

            if (deleting && charIndex > 0) {
                charIndex -= 1;
                window.setTimeout(tick, deletingSpeed);
                return;
            }

            deleting = false;
            phraseIndex = (phraseIndex + 1) % phrases.length;
            window.setTimeout(tick, 220);
        };

        tick();
    };

    const initTyping = () => {
        startTypingEffect(splashTypedText, [
            'loading cinematic AI-engineer visuals',
            'preparing recruiter-ready software branding',
            'activating Pavilson Is Here assistant',
        ]);

        startTypingEffect(heroTypedText, [
            'building Python backends, AI workflows, and premium web experiences',
            'turning project thinking into recruiter-ready product storytelling',
            'shipping immersive interfaces without sacrificing practical engineering',
        ], {
            typingSpeed: 40,
            deletingSpeed: 20,
            holdDelay: 1600,
        });
    };

    const initSplash = () => {
        const revealPortfolio = () => {
            body.classList.remove('is-splash-active');
            body.classList.add('is-entered');
            splashScreen?.classList.add('is-hidden');
        };

        const enterPortfolio = () => {
            if (hasEntered) {
                return;
            }

            hasEntered = true;
            enterPortfolioButton?.setAttribute('disabled', 'disabled');

            if (typeof gsap === 'undefined' || prefersReducedMotion) {
                revealPortfolio();
                return;
            }

            const timeline = gsap.timeline({
                onComplete: revealPortfolio,
            });

            timeline
                .to('.splash-panel > *', {
                    opacity: 0,
                    y: -18,
                    stagger: 0.05,
                    duration: 0.36,
                    ease: 'power2.in',
                })
                .to('.splash-panel', {
                    opacity: 0,
                    scale: 1.02,
                    duration: 0.4,
                    ease: 'power2.inOut',
                }, '<');
        };

        enterPortfolioButton?.addEventListener('click', enterPortfolio);

        document.addEventListener('keydown', (event) => {
            const target = event.target;
            const isTyping = target instanceof HTMLElement && ['INPUT', 'TEXTAREA'].includes(target.tagName);

            if (!isTyping && event.key === 'Enter' && body.classList.contains('is-splash-active')) {
                enterPortfolio();
            }
        });
    };

    const initNav = () => {
        navToggle?.addEventListener('click', () => {
            const shouldOpen = !navPanel?.classList.contains('is-open');
            setNavOpen(Boolean(shouldOpen));
        });

        document.querySelectorAll('.nav-links a').forEach((link) => {
            link.addEventListener('click', () => setNavOpen(false));
        });

        document.addEventListener('click', (event) => {
            if (!navPanel || !navToggle) {
                return;
            }

            const target = event.target;
            if (!(target instanceof Node)) {
                return;
            }

            if (!navPanel.contains(target) && !navToggle.contains(target)) {
                setNavOpen(false);
            }
        });
    };

    const initActiveNav = () => {
        const links = Array.from(document.querySelectorAll('.nav-links a'));
        const linkMap = new Map(
            links
                .map((link) => [link.getAttribute('href')?.replace('#', ''), link])
                .filter(([id]) => Boolean(id))
        );
        const sections = Array.from(document.querySelectorAll('main section[id]'));

        if (!sections.length) {
            return;
        }

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) {
                    return;
                }

                links.forEach((link) => link.classList.remove('is-active'));
                linkMap.get(entry.target.id)?.classList.add('is-active');
            });
        }, {
            threshold: 0.35,
            rootMargin: '-15% 0px -45% 0px',
        });

        sections.forEach((section) => observer.observe(section));
    };

    const initReveals = () => {
        const revealElements = document.querySelectorAll('[data-reveal]');

        if (!revealElements.length) {
            return;
        }

        if (prefersReducedMotion || typeof gsap === 'undefined') {
            revealElements.forEach((element) => {
                element.style.opacity = '1';
                element.style.transform = 'none';
            });
            return;
        }

        if (typeof ScrollTrigger !== 'undefined') {
            gsap.registerPlugin(ScrollTrigger);
        }

        gsap.utils.toArray('[data-reveal]').forEach((element) => {
            gsap.fromTo(element, {
                opacity: 0,
                y: 28,
            }, {
                opacity: 1,
                y: 0,
                duration: 0.9,
                ease: 'power3.out',
                scrollTrigger: typeof ScrollTrigger === 'undefined' ? undefined : {
                    trigger: element,
                    start: 'top 84%',
                    once: true,
                },
            });
        });
    };

    const initTilt = () => {
        const cards = document.querySelectorAll('[data-tilt]');

        if (!cards.length || prefersReducedMotion || !window.matchMedia('(pointer: fine)').matches) {
            return;
        }

        cards.forEach((card) => {
            card.addEventListener('pointermove', (event) => {
                const bounds = card.getBoundingClientRect();
                const x = (event.clientX - bounds.left) / bounds.width;
                const y = (event.clientY - bounds.top) / bounds.height;
                const rotateY = (x - 0.5) * 12;
                const rotateX = (0.5 - y) * 10;
                card.style.transform = `perspective(1200px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-6px)`;
            });

            card.addEventListener('pointerleave', () => {
                card.style.transform = '';
            });
        });
    };

    const appendChatMessage = (role, message, options = {}) => {
        const messageHost = getChatMessageHost();
        if (!messageHost) {
            return null;
        }

        const wrapper = document.createElement('article');
        wrapper.className = `chat-message ${role === 'user' ? 'chat-message-user' : 'chat-message-bot'}`;

        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble';

        const content = document.createElement('div');
        content.className = 'chat-bubble__content';
        content.textContent = message;
        bubble.appendChild(content);

        if (Array.isArray(options.actions) && options.actions.length) {
            const actions = document.createElement('div');
            actions.className = 'chat-actions';

            options.actions.forEach((action) => {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'chat-action-button';
                button.dataset.actionKind = action.kind;
                button.dataset.actionValue = action.value;
                button.textContent = action.label;
                actions.appendChild(button);
            });

            bubble.appendChild(actions);
        }

        if (Array.isArray(options.suggestedPrompts) && options.suggestedPrompts.length) {
            const suggestions = document.createElement('div');
            suggestions.className = 'chat-actions';

            options.suggestedPrompts.forEach((prompt) => {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'chat-action-button';
                button.dataset.actionKind = 'prompt';
                button.dataset.actionValue = prompt;
                button.textContent = prompt;
                suggestions.appendChild(button);
            });

            bubble.appendChild(suggestions);
        }

        wrapper.appendChild(bubble);
        messageHost.appendChild(wrapper);
        scrollChatToLatest();
        return wrapper;
    };

    const createTypingBubble = () => {
        const messageHost = getChatMessageHost();
        if (!messageHost) {
            return null;
        }

        const wrapper = document.createElement('article');
        wrapper.className = 'chat-message chat-message-bot';

        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble';

        const typing = document.createElement('div');
        typing.className = 'typing-indicator';
        typing.innerHTML = '<span></span><span></span><span></span>';
        bubble.appendChild(typing);
        wrapper.appendChild(bubble);
        messageHost.appendChild(wrapper);
        scrollChatToLatest();
        return wrapper;
    };

    const replaceTypingBubble = (typingBubble, payload) => {
        if (!typingBubble) {
            appendChatMessage('bot', payload.response, {
                actions: payload.actions,
                suggestedPrompts: payload.suggested_prompts,
            });
            return;
        }

        typingBubble.remove();
        appendChatMessage('bot', payload.response, {
            actions: payload.actions,
            suggestedPrompts: payload.suggested_prompts,
        });
    };

    const runChatAction = (kind, value) => {
        switch (kind) {
        case 'navigate':
            smoothScrollToSection(value);
            break;
        case 'download':
            if (value === 'resume' && appData.resumeUrl) {
                window.open(appData.resumeUrl, '_blank', 'noopener');
            }
            if (value === 'certificate' && appData.certificateUrl) {
                window.open(appData.certificateUrl, '_blank', 'noopener');
            }
            break;
        case 'contact':
            if (value === 'email') {
                window.location.href = `mailto:${appData.email}`;
            }
            if (value === 'phone' && appData.phoneLink) {
                window.location.href = appData.phoneLink;
            }
            if (value === 'linkedin' && appData.linkedin) {
                window.open(appData.linkedin, '_blank', 'noopener');
            }
            break;
        case 'prompt':
            requestAssistant(value);
            break;
        default:
            break;
        }
    };

    const requestAssistant = async (message, options = {}) => {
        if (!message || !sendButton) {
            return;
        }

        setChatOpen(true);

        if (!options.silentUser) {
            appendChatMessage('user', message);
        }

        sendButton.disabled = true;
        if (userInput) {
            userInput.value = '';
            autoResizeTextarea();
        }

        const typingBubble = createTypingBubble();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            const payload = await response.json();

            if (!response.ok) {
                throw new Error(payload.response || `Request failed with status ${response.status}`);
            }

            replaceTypingBubble(typingBubble, payload);
        } catch (error) {
            replaceTypingBubble(typingBubble, {
                response: 'The assistant is temporarily unavailable. Please try again in a moment.',
                actions: [
                    { kind: 'navigate', value: 'contact', label: 'Open contact' },
                    { kind: 'navigate', value: 'resume', label: 'Open resume' },
                ],
                suggested_prompts: [],
            });
            console.error('Assistant request failed:', error);
        } finally {
            sendButton.disabled = false;
            userInput?.focus();
        }
    };

    const autoResizeTextarea = () => {
        if (!userInput) {
            return;
        }

        userInput.style.height = 'auto';
        userInput.style.height = `${Math.min(userInput.scrollHeight, 144)}px`;
    };

    const initChat = () => {
        chatToggle?.addEventListener('click', () => {
            const shouldOpen = !chatContainer?.classList.contains('is-open');
            setChatOpen(Boolean(shouldOpen));
        });

        chatClose?.addEventListener('click', () => setChatOpen(false));

        document.querySelectorAll('[data-chat-open="true"]').forEach((button) => {
            button.addEventListener('click', () => setChatOpen(true));
        });

        document.querySelectorAll('[data-chat-prompt]').forEach((button) => {
            button.addEventListener('click', () => {
                requestAssistant(button.getAttribute('data-chat-prompt') || '');
            });
        });

        chatMessages?.addEventListener('click', (event) => {
            const target = event.target;
            if (!(target instanceof HTMLElement) || !target.classList.contains('chat-action-button')) {
                return;
            }

            runChatAction(target.dataset.actionKind || '', target.dataset.actionValue || '');
        });

        chatForm?.addEventListener('submit', async (event) => {
            event.preventDefault();
            const message = userInput?.value.trim();
            if (!message) {
                userInput?.focus();
                return;
            }

            await requestAssistant(message);
        });

        userInput?.addEventListener('input', autoResizeTextarea);

        userInput?.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                chatForm?.requestSubmit();
            }
        });

        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape') {
                setChatOpen(false);
                setNavOpen(false);
            }
        });

        autoResizeTextarea();
        scrollChatToLatest('auto');
    };

    const initHeroParallax = () => {
        if (prefersReducedMotion || !window.matchMedia('(pointer: fine)').matches) {
            return;
        }

        const heroVisual = document.querySelector('.hero-visual');
        const portrait = document.querySelector('.hero-portrait');

        window.addEventListener('pointermove', (event) => {
            pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
            pointer.y = (event.clientY / window.innerHeight) * 2 - 1;
        }, { passive: true });

        const animate = () => {
            if (heroVisual) {
                heroVisual.style.transform = `translate3d(${pointer.x * 10}px, ${pointer.y * -8}px, 0)`;
            }

            if (portrait) {
                portrait.style.transform = `rotateY(${pointer.x * 8}deg) rotateX(${pointer.y * -6}deg)`;
            }

            window.requestAnimationFrame(animate);
        };

        animate();
    };

    const initThreeScene = () => {
        const canvas = document.getElementById('bg');

        if (!canvas || typeof THREE === 'undefined') {
            return;
        }

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(48, window.innerWidth / window.innerHeight, 0.1, 100);
        const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.8));
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setClearColor(0x000000, 0);

        camera.position.z = 8;

        const group = new THREE.Group();
        scene.add(group);

        const cube = new THREE.Mesh(
            new THREE.BoxGeometry(1.25, 1.25, 1.25),
            new THREE.MeshPhysicalMaterial({
                color: 0x38bdf8,
                metalness: 0.4,
                roughness: 0.12,
                transmission: 0.28,
                transparent: true,
                opacity: 0.9,
                emissive: 0x0891b2,
                emissiveIntensity: 0.35,
            })
        );
        cube.position.set(-1.25, 0.5, -0.2);
        group.add(cube);

        const torus = new THREE.Mesh(
            new THREE.TorusGeometry(2.3, 0.12, 20, 120),
            new THREE.MeshStandardMaterial({
                color: 0x8b5cf6,
                metalness: 0.55,
                roughness: 0.3,
                emissive: 0x6d28d9,
                emissiveIntensity: 0.4,
            })
        );
        torus.rotation.x = 1.2;
        torus.position.set(1.2, 0.2, -0.8);
        group.add(torus);

        const sphere = new THREE.Mesh(
            new THREE.SphereGeometry(0.55, 24, 24),
            new THREE.MeshPhysicalMaterial({
                color: 0xffffff,
                transparent: true,
                opacity: 0.28,
                transmission: 0.4,
                roughness: 0.1,
                emissive: 0x38bdf8,
                emissiveIntensity: 0.22,
            })
        );
        sphere.position.set(2.7, -1.25, -1.4);
        group.add(sphere);

        const ambient = new THREE.AmbientLight(0xbfe9ff, 0.8);
        scene.add(ambient);

        const cyanLight = new THREE.PointLight(0x38bdf8, 2.2, 40, 2);
        cyanLight.position.set(3.8, 3.2, 5);
        scene.add(cyanLight);

        const purpleLight = new THREE.PointLight(0x8b5cf6, 1.8, 40, 2);
        purpleLight.position.set(-3.4, -2.1, 4.8);
        scene.add(purpleLight);

        const particleGeometry = new THREE.BufferGeometry();
        const particleCount = 700;
        const positions = new Float32Array(particleCount * 3);

        for (let index = 0; index < positions.length; index += 3) {
            positions[index] = (Math.random() - 0.5) * 36;
            positions[index + 1] = (Math.random() - 0.5) * 24;
            positions[index + 2] = (Math.random() - 0.5) * 18;
        }

        particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

        const particles = new THREE.Points(
            particleGeometry,
            new THREE.PointsMaterial({
                color: 0xc6f0ff,
                size: 0.035,
                transparent: true,
                opacity: 0.76,
                blending: THREE.AdditiveBlending,
                depthWrite: false,
            })
        );
        particles.position.z = -4;
        scene.add(particles);

        const clock = new THREE.Clock();

        const onResize = () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.position.z = window.innerWidth < 720 ? 10 : 8;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        };

        window.addEventListener('resize', onResize, { passive: true });
        onResize();

        const render = () => {
            const elapsed = clock.getElapsedTime();

            if (!prefersReducedMotion) {
                cube.rotation.x = elapsed * 0.5;
                cube.rotation.y = elapsed * 0.8;
                cube.position.y = 0.45 + Math.sin(elapsed * 1.1) * 0.24;

                torus.rotation.z = elapsed * 0.28;
                torus.rotation.y = Math.sin(elapsed * 0.5) * 0.32;
                torus.position.y = 0.2 + Math.cos(elapsed * 0.9) * 0.16;

                sphere.position.y = -1.25 + Math.sin(elapsed * 0.85) * 0.22;
                sphere.rotation.y = elapsed * 0.3;

                group.rotation.y += ((pointer.x * 0.18) - group.rotation.y) * 0.04;
                group.rotation.x += ((pointer.y * -0.12) - group.rotation.x) * 0.04;
                group.position.x += ((pointer.x * 0.7) - group.position.x) * 0.03;
                group.position.y += ((pointer.y * -0.35) - group.position.y) * 0.03;

                particles.rotation.y = elapsed * 0.02;
                particles.rotation.x = elapsed * 0.015;
            }

            renderer.render(scene, camera);
            window.requestAnimationFrame(render);
        };

        render();
    };

    initTyping();
    initSplash();
    initNav();
    initActiveNav();
    initReveals();
    initTilt();
    initChat();
    initHeroParallax();
    initThreeScene();
    autoResizeTextarea();
});
