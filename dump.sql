--
-- PostgreSQL database dump
--

-- Dumped from database version 15.0
-- Dumped by pg_dump version 15.0

-- Started on 2022-12-11 22:11:55

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- TOC entry 215 (class 1259 OID 24670)
-- Name: contacts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contacts (
    id integer NOT NULL,
    number character varying(15) NOT NULL,
    operator_code integer NOT NULL,
    tag character varying(100),
    time_zone character varying(10)
);


ALTER TABLE public.contacts OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 24669)
-- Name: contacts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contacts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contacts_id_seq OWNER TO postgres;

--
-- TOC entry 3357 (class 0 OID 0)
-- Dependencies: 214
-- Name: contacts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contacts_id_seq OWNED BY public.contacts.id;


--
-- TOC entry 219 (class 1259 OID 24684)
-- Name: mailings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mailings (
    id integer NOT NULL,
    start_time timestamp without time zone NOT NULL,
    message text NOT NULL,
    filters character varying(200) NOT NULL,
    end_time timestamp without time zone NOT NULL
);


ALTER TABLE public.mailings OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 24683)
-- Name: mailings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mailings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mailings_id_seq OWNER TO postgres;

--
-- TOC entry 3358 (class 0 OID 0)
-- Dependencies: 218
-- Name: mailings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mailings_id_seq OWNED BY public.mailings.id;


--
-- TOC entry 217 (class 1259 OID 24677)
-- Name: messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.messages (
    id integer NOT NULL,
    datetime timestamp without time zone NOT NULL,
    status character varying(20),
    mailing_id integer NOT NULL,
    contact_id integer NOT NULL
);


ALTER TABLE public.messages OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 24676)
-- Name: messages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.messages_id_seq OWNER TO postgres;

--
-- TOC entry 3359 (class 0 OID 0)
-- Dependencies: 216
-- Name: messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.messages_id_seq OWNED BY public.messages.id;


--
-- TOC entry 221 (class 1259 OID 24693)
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    login character varying(128) NOT NULL,
    password character varying(255) NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 24692)
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO postgres;

--
-- TOC entry 3360 (class 0 OID 0)
-- Dependencies: 220
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- TOC entry 3188 (class 2604 OID 24673)
-- Name: contacts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts ALTER COLUMN id SET DEFAULT nextval('public.contacts_id_seq'::regclass);


--
-- TOC entry 3190 (class 2604 OID 24687)
-- Name: mailings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mailings ALTER COLUMN id SET DEFAULT nextval('public.mailings_id_seq'::regclass);


--
-- TOC entry 3189 (class 2604 OID 24680)
-- Name: messages id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages ALTER COLUMN id SET DEFAULT nextval('public.messages_id_seq'::regclass);


--
-- TOC entry 3191 (class 2604 OID 24696)
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- TOC entry 3345 (class 0 OID 24670)
-- Dependencies: 215
-- Data for Name: contacts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contacts (id, number, operator_code, tag, time_zone) FROM stdin;
11	+79203568132	920	tag2	+2
12	+79024563452	902	tag3	+3
50	+79176123981	917	tag1	+2
51	+79208543421	920	tag2	+4
7	+79176159280	917	tag1	+5
\.


--
-- TOC entry 3349 (class 0 OID 24684)
-- Dependencies: 219
-- Data for Name: mailings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mailings (id, start_time, message, filters, end_time) FROM stdin;
2	2022-12-11 06:30:00	Доброе утро	tag1, tag2, tag3	2022-12-20 09:30:00
3	2022-12-11 18:00:00	Добрый вечер	tag1, tag2, tag3	2022-12-20 21:30:00
20	2022-12-11 09:30:00	Добрый день	tag1, tag2, tag3	2022-12-20 18:00:00
21	2022-12-11 10:30:00	Какой-то текст	tag1, tag3	2022-12-20 17:00:00
\.


--
-- TOC entry 3347 (class 0 OID 24677)
-- Dependencies: 217
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.messages (id, datetime, status, mailing_id, contact_id) FROM stdin;
\.


--
-- TOC entry 3351 (class 0 OID 24693)
-- Dependencies: 221
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, login, password) FROM stdin;
1	admin	pbkdf2:sha256:260000$gz2djQfucahajIHl$f3a61a8bdc2b7d5ebac4e5465828f31a5514311e321bcc29c410b39ed0dd2f3f
\.


--
-- TOC entry 3361 (class 0 OID 0)
-- Dependencies: 214
-- Name: contacts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contacts_id_seq', 51, true);


--
-- TOC entry 3362 (class 0 OID 0)
-- Dependencies: 218
-- Name: mailings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mailings_id_seq', 21, true);


--
-- TOC entry 3363 (class 0 OID 0)
-- Dependencies: 216
-- Name: messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.messages_id_seq', 71, true);


--
-- TOC entry 3364 (class 0 OID 0)
-- Dependencies: 220
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 1, true);


--
-- TOC entry 3193 (class 2606 OID 24675)
-- Name: contacts contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT contacts_pkey PRIMARY KEY (id);


--
-- TOC entry 3197 (class 2606 OID 24691)
-- Name: mailings mailings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mailings
    ADD CONSTRAINT mailings_pkey PRIMARY KEY (id);


--
-- TOC entry 3195 (class 2606 OID 24682)
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- TOC entry 3199 (class 2606 OID 24700)
-- Name: user user_login_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_login_key UNIQUE (login);


--
-- TOC entry 3201 (class 2606 OID 24698)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


-- Completed on 2022-12-11 22:11:56

--
-- PostgreSQL database dump complete
--

