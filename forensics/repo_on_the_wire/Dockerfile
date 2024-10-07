FROM ubuntu

RUN apt update -y && apt install -y git
WORKDIR root
COPY generate.sh .
RUN chmod +x generate.sh && ./generate.sh TUDCTF{it5_2024_u53_55h_4nd_n0t_g1t_pr0t0c01}
WORKDIR /srv/git
RUN ln -s /root/repo/.git /srv/git/flagrepo.git

EXPOSE 9418
CMD git daemon --reuseaddr --base-path=/srv/git/ /srv/git/
