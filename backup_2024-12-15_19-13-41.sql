--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: customer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customer (
    customer_id integer NOT NULL,
    name character varying(255) NOT NULL,
    surname character varying(255) NOT NULL,
    phone character varying(50) NOT NULL,
    email character varying(255) NOT NULL
);


ALTER TABLE public.customer OWNER TO postgres;

--
-- Name: customer_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.customer_customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.customer_customer_id_seq OWNER TO postgres;

--
-- Name: customer_customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.customer_customer_id_seq OWNED BY public.customer.customer_id;


--
-- Name: direction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.direction (
    direction_id integer NOT NULL,
    start character varying(255) NOT NULL,
    finish character varying(255) NOT NULL,
    "time" time without time zone NOT NULL,
    distance real NOT NULL
);


ALTER TABLE public.direction OWNER TO postgres;

--
-- Name: direction_direction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.direction_direction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.direction_direction_id_seq OWNER TO postgres;

--
-- Name: direction_direction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.direction_direction_id_seq OWNED BY public.direction.direction_id;


--
-- Name: sale; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sale (
    sale_id integer NOT NULL,
    sale_credits real NOT NULL,
    date date NOT NULL,
    ticket_office_id integer,
    ticket_id integer NOT NULL
);


ALTER TABLE public.sale OWNER TO postgres;

--
-- Name: sale_sale_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sale_sale_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sale_sale_id_seq OWNER TO postgres;

--
-- Name: sale_sale_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sale_sale_id_seq OWNED BY public.sale.sale_id;


--
-- Name: seat; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.seat (
    seat_id integer NOT NULL,
    class_field character varying(255) NOT NULL,
    seat_place integer NOT NULL,
    carriage integer NOT NULL,
    train_id integer NOT NULL
);


ALTER TABLE public.seat OWNER TO postgres;

--
-- Name: seat_seat_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.seat_seat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.seat_seat_id_seq OWNER TO postgres;

--
-- Name: seat_seat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.seat_seat_id_seq OWNED BY public.seat.seat_id;


--
-- Name: ticket; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ticket (
    ticket_id integer NOT NULL,
    date date NOT NULL,
    direction_id integer,
    train_id integer,
    seat_id integer,
    customer_id integer NOT NULL
);


ALTER TABLE public.ticket OWNER TO postgres;

--
-- Name: ticket_ticket_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ticket_ticket_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ticket_ticket_id_seq OWNER TO postgres;

--
-- Name: ticket_ticket_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ticket_ticket_id_seq OWNED BY public.ticket.ticket_id;


--
-- Name: ticketoffice; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ticketoffice (
    ticket_office_id integer NOT NULL,
    place character varying(255) NOT NULL
);


ALTER TABLE public.ticketoffice OWNER TO postgres;

--
-- Name: ticketoffice_ticket_office_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ticketoffice_ticket_office_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ticketoffice_ticket_office_id_seq OWNER TO postgres;

--
-- Name: ticketoffice_ticket_office_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ticketoffice_ticket_office_id_seq OWNED BY public.ticketoffice.ticket_office_id;


--
-- Name: train; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.train (
    train_id integer NOT NULL,
    train_type character varying(255) NOT NULL,
    rate real NOT NULL,
    direction_id integer
);


ALTER TABLE public.train OWNER TO postgres;

--
-- Name: train_train_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.train_train_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.train_train_id_seq OWNER TO postgres;

--
-- Name: train_train_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.train_train_id_seq OWNED BY public.train.train_id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    is_admin boolean NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: customer customer_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customer ALTER COLUMN customer_id SET DEFAULT nextval('public.customer_customer_id_seq'::regclass);


--
-- Name: direction direction_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.direction ALTER COLUMN direction_id SET DEFAULT nextval('public.direction_direction_id_seq'::regclass);


--
-- Name: sale sale_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sale ALTER COLUMN sale_id SET DEFAULT nextval('public.sale_sale_id_seq'::regclass);


--
-- Name: seat seat_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seat ALTER COLUMN seat_id SET DEFAULT nextval('public.seat_seat_id_seq'::regclass);


--
-- Name: ticket ticket_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ticket ALTER COLUMN ticket_id SET DEFAULT nextval('public.ticket_ticket_id_seq'::regclass);


--
-- Name: ticketoffice ticket_office_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ticketoffice ALTER COLUMN ticket_office_id SET DEFAULT nextval('public.ticketoffice_ticket_office_id_seq'::regclass);


--
-- Name: train train_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.train ALTER COLUMN train_id SET DEFAULT nextval('public.train_train_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: customer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.customer (customer_id, name, surname, phone, email) FROM stdin;
1	Иван	Иванов	88005553535	example@example.com
2	Мария	Эдмурова	89511751523	abv@gmail.com
3	Кто-то	Кто-тов	88888888888	123@123.123
4	Петр	Петров	89123456780	petr@mail.ru
5	Елена	Сидорова	89001112233	elena@gmail.com
6	Алексей	Смирнов	89555555555	alexey@yandex.ru
7	Светлана	Кузнецова	89012345678	svetlana@inbox.ru
8	Дмитрий	Попов	89999999999	dima@mail.ru
9	Ольга	Соколова	88001002003	olga@example.com
10	Сергей	Васильев	89501234567	sergey@yandex.ru
11	Дмитрий	Чайка	89994217321	test@test.test
12	Дмитрий	Чайка	89994217321	test@test.test
13	Дмитрий	Чайка	89994217321	test@test.test
14	Анастасия	Каменщикова	88005553536	aok@kk.kk
17	Евлампий	Прохоров	89522525252	evlmp@evlmp.evlmp
\.


--
-- Data for Name: direction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.direction (direction_id, start, finish, "time", distance) FROM stdin;
1	Москва	Санкт-Петербург	05:45:45	158.25
2	Старт	Финиш	00:00:01	0.1
3	Тут	Там	02:00:00	5
4	Город А	Город Б	10:00:00	200.5
5	Пункт X	Пункт Y	14:30:00	350
6	Место 1	Место 2	12:15:00	100
7	Станция А	Станция Б	08:45:00	150.75
8	Точка P	Точка Q	00:30:00	5.3
9	Регион 1	Регион 2	16:00:00	400
10	Зона 1	Зона 2	09:00:00	250.25
\.


--
-- Data for Name: sale; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sale (sale_id, sale_credits, date, ticket_office_id, ticket_id) FROM stdin;
1	1500	2023-10-16	1	1
2	28.5	2021-01-25	2	2
3	159.68	2022-05-12	3	3
4	85.75	2024-02-21	4	4
5	120	2023-11-11	5	5
6	90.5	2022-08-06	6	6
7	115.2	2024-01-16	7	7
8	275	2023-07-01	8	8
9	45	2022-12-26	9	9
10	180.8	2024-04-02	10	10
11	180.8	2024-04-02	10	11
12	2373.75	2024-12-23	1	12
13	3753.75	2024-12-25	1	13
14	79.5	2024-12-21	9	14
15	1.5	2024-12-31	7	15
\.


--
-- Data for Name: seat; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.seat (seat_id, class_field, seat_place, carriage, train_id) FROM stdin;
1	С	1	1	1
2	СВ	1	1	2
3	2 класс	1	1	3
4	Первый	1	1	4
5	Второй	1	1	5
6	Купе	1	1	6
7	Плацкарт	1	1	7
8	Люкс	1	1	8
9	Общий	1	1	9
10	Бизнес	1	1	10
11	С	1	1	10
\.


--
-- Data for Name: ticket; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ticket (ticket_id, date, direction_id, train_id, seat_id, customer_id) FROM stdin;
1	2023-10-15	1	1	1	1
2	2021-01-01	2	2	2	2
3	2022-05-12	3	3	3	3
4	2024-02-20	4	4	4	4
5	2023-11-10	5	5	5	5
6	2022-08-05	6	6	6	6
7	2024-01-15	7	7	7	7
8	2023-06-30	8	8	8	8
9	2022-12-25	9	9	9	9
10	2024-04-01	10	10	10	10
11	2024-09-25	10	10	11	1
12	2024-12-23	1	\N	1	11
13	2024-12-25	10	\N	10	12
14	2024-12-21	8	8	8	13
15	2024-12-31	2	2	2	17
\.


--
-- Data for Name: ticketoffice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ticketoffice (ticket_office_id, place) FROM stdin;
1	Москва
2	Старт
3	Тут
4	Вокзал А
5	Касса X
6	Офис 1
7	Терминал B
8	Платформа C
9	Здание D
10	Участок E
\.


--
-- Data for Name: train; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.train (train_id, train_type, rate, direction_id) FROM stdin;
1	Скорый	0	1
2	Пригородный	0	2
3	Местного сообщения	0	3
4	Экспресс	0	4
5	Региональный	0	5
6	Пассажирский	0	6
7	Скоростной	0	7
8	Магистральный	0	8
9	Грузовой	0	9
10	Межобластной	0	10
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, username, password, is_admin) FROM stdin;
5	forelken	$2b$12$dCBBQTD8ef1VLYDJlizBfuEfFtgRnqddsFzEvkjS2VseHl3LYWAjm	t
4	admin	$2b$12$sS5kOU1STgy1aLdpFOiot.3iU1G8AAWLc1K01xKx3eP.84Nosl6Ua	t
6	username	$2b$12$VEgb8gvXCLeHd/DxoyRl4OeT.jYRqZe.AjK0vfz/3CL9QwYzbuOta	t
\.


--
-- Name: customer_customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customer_customer_id_seq', 17, true);


--
-- Name: direction_direction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.direction_direction_id_seq', 10, true);


--
-- Name: sale_sale_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sale_sale_id_seq', 15, true);


--
-- Name: seat_seat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.seat_seat_id_seq', 11, true);


--
-- Name: ticket_ticket_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ticket_ticket_id_seq', 15, true);


--
-- Name: ticketoffice_ticket_office_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ticketoffice_ticket_office_id_seq', 11, true);


--
-- Name: train_train_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.train_train_id_seq', 10, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 6, true);


--
-- Name: customer customer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (customer_id);


--
-- Name: direction direction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.direction
    ADD CONSTRAINT direction_pkey PRIMARY KEY (direction_id);


--
-- Name: sale sale_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sale
    ADD CONSTRAINT sale_pkey PRIMARY KEY (sale_id);


--
-- Name: seat seat_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seat
    ADD CONSTRAINT seat_pkey PRIMARY KEY (seat_id);


--
-- Name: ticket ticket_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ticket
    ADD CONSTRAINT ticket_pkey PRIMARY KEY (ticket_id);


--
-- Name: ticketoffice ticketoffice_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ticketoffice
    ADD CONSTRAINT ticketoffice_pkey PRIMARY KEY (ticket_office_id);


--
-- Name: train train_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.train
    ADD CONSTRAINT train_pkey PRIMARY KEY (train_id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: sale_ticket_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sale_ticket_id ON public.sale USING btree (ticket_id);


--
-- Name: sale_ticket_office_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sale_ticket_office_id ON public.sale USING btree (ticket_office_id);


--
-- Name: seat_train_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX seat_train_id ON public.seat USING btree (train_id);


--
-- Name: ticket_customer_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ticket_customer_id ON public.ticket USING btree (customer_id);


--
-- Name: ticket_direction_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ticket_direction_id ON public.ticket USING btree (direction_id);


--
-- Name: ticket_seat_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ticket_seat_id ON public.ticket USING btree (seat_id);


--
-- Name: ticket_train_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ticket_train_id ON public.ticket USING btree (train_id);


--
-- Name: train_direction_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX train_direction_id ON public.train USING btree (direction_id);


--
-- Name: sale sale_ticket_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sale
    ADD CONSTRAINT sale_ticket_id_fkey FOREIGN KEY (ticket_id) REFERENCES public.ticket(ticket_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sale sale_ticket_office_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sale
    ADD CONSTRAINT sale_ticket_office_id_fkey FOREIGN KEY (ticket_office_id) REFERENCES public.ticketoffice(ticket_office_id) ON DELETE SET NULL;


--
-- Name: seat seat_train_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seat
    ADD CONSTRAINT seat_train_id_fkey FOREIGN KEY (train_id) REFERENCES public.train(train_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ticket ticket_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ticket
    ADD CONSTRAINT ticket_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customer(customer_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ticket ticket_direction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ticket
    ADD CONSTRAINT ticket_direction_id_fkey FOREIGN KEY (direction_id) REFERENCES public.direction(direction_id) ON DELETE SET NULL;


--
-- Name: ticket ticket_seat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ticket
    ADD CONSTRAINT ticket_seat_id_fkey FOREIGN KEY (seat_id) REFERENCES public.seat(seat_id) ON DELETE SET NULL;


--
-- Name: ticket ticket_train_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ticket
    ADD CONSTRAINT ticket_train_id_fkey FOREIGN KEY (train_id) REFERENCES public.train(train_id) ON DELETE SET NULL;


--
-- Name: train train_direction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.train
    ADD CONSTRAINT train_direction_id_fkey FOREIGN KEY (direction_id) REFERENCES public.direction(direction_id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

